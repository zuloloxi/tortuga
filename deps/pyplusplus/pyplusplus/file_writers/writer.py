# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""defines interface for all classes that writes L{code_creators.module_t} to file(s)"""

import os
import time
from pyplusplus import _logging_
from pyplusplus import code_creators
from pyplusplus import code_repository

class writer_t(object):
    """Base class for all module/code writers.
    
    All writers should have similar usage::
    
      w = writer_class(module, file, ...)
      w.write()
    """
    logger = _logging_.loggers.file_writer
    
    def __init__(self, extmodule):
        object.__init__(self)
        self.__extmodule = extmodule
        
        
    def _get_extmodule(self):
        return self.__extmodule
    extmodule = property( _get_extmodule,
                          doc="""The root of the code creator tree.
                          @type: module_t""")
    
    def write(self):
        """ Main write method.  Should be overridden by derived classes. """
        raise NotImplementedError()
       
    @staticmethod
    def create_backup(fpath):
        """creates backup of the file, by renaming it to C{fpath + ~}"""
        if not os.path.exists( fpath ):
            return         
        backup_fpath = fpath + '~'
        if os.path.exists( backup_fpath ):
            os.remove( backup_fpath )
        os.rename( fpath, backup_fpath )
    
    def write_code_repository(self, dir):
        """creates files defined in L{code_repository} package"""
        system_headers = self.extmodule.get_system_headers( recursive=True )
        for cr in code_repository.all:
            if cr.file_name in system_headers:
                #check whether file from code repository is used
                self.write_file( os.path.join( dir, cr.file_name ), cr.code )
        #named_tuple.py is a special case :-(
        self.write_file( os.path.join( dir, code_repository.named_tuple.file_name )
                         , code_repository.named_tuple.code ) 
    @staticmethod
    def write_file( fpath, content ):
        """Write a source file.

        This method writes the string content into the specified file.
        An additional fixed header is written at the top of the file before
        content.

        @param fpath: File name
        @type fpath: str
        @param content: The content of the file
        @type content: str
        """
        fname = os.path.split( fpath )[1]
        writer_t.logger.debug( 'write code to file "%s" - started' % fpath )
        start_time = time.clock()
        fcontent_new = []
        if os.path.splitext( fpath )[1] == '.py':
            fcontent_new.append( '# This file has been generated by Py++.' )
        else:
            fcontent_new.append( '// This file has been generated by Py++.' )
        fcontent_new.append( os.linesep * 2 )
        fcontent_new.append( content )
        fcontent_new.append( os.linesep ) #keep gcc happy
        fcontent_new = ''.join( fcontent_new )
        
        if os.path.exists( fpath ):
            #small optimization to cut down compilation time
            f = file( fpath, 'rb' )
            fcontent = f.read()
            f.close()
            if fcontent == fcontent_new:
                writer_t.logger.debug( 'file was not changed - done( %f seconds )'
                                       % ( time.clock() - start_time ) )
                return
        else:
            writer_t.logger.debug( 'file does not exist' )
            
        writer_t.create_backup( fpath )
        f = file( fpath, 'w+b' )
        f.write( fcontent_new )
        f.close()
        writer_t.logger.info( 'file "%s" - updated( %f seconds )' % ( fname, time.clock() - start_time ) )
    
    def get_user_headers( self, creators ):
        headers = []
        creators = filter( lambda creator: isinstance( creator, code_creators.declaration_based_t )
                           , creators )
        map( lambda creator: headers.extend( creator.get_user_headers() )
             , creators )
        return code_creators.code_creator_t.unique_headers( headers )