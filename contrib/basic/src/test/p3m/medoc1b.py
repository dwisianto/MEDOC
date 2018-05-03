
#
#
#
import os
import re
import sys
import time
import logging
import unittest
import configparser


logging.basicConfig(level=logging.DEBUG)
sys.path.append('/Users/dsm/DGit/d.bee.whcs/b9/y9/rnk18a/rk8.ex.medoc1a/src/main/p3/medoc/lib')
import MEDOC
import getters


#
#
##
class medoc1(unittest.TestCase):

    cfg_file='../p3resource/configuration1b.cfg'
    file_downloaded_custom = 'pubmed18n0001.xml.gz'
    insert_limit=3

    def m101a_cfg(self):
        ''' ensure the parameters can be initilized from configurations
        in  : configuration.cfg
        out : parameters, insert_limit, insert_log_path
        '''
        logging.debug('m110a_cfg' )
        parameters = configparser.ConfigParser()
        parameters.read(self.cfg_file)
        logging.debug( parameters.sections() )

        insert_limit = int(parameters['database']['insert_command_limit'])
        insert_log_path = os.path.join(parameters['paths']['program_path'], parameters['paths']['already_downloaded_files'])
        download_folder = os.path.join(parameters['paths']['program_path'], parameters['paths']['pubmed_data_download'])
        logging.debug( insert_limit )
        logging.debug( insert_log_path )
        logging.debug( download_folder)

    def m102a_init(self):
        ''' create a database in mysql
        in : configuration.cfg
        out : none
        '''
        logging.debug('m102a_init' )
        logging.debug(sys.path)
        myMedoc = MEDOC.MEDOC(self.cfg_file)

        # StepA : Create database if not exist
        myMedoc.create_pubmedDB()
        #myMedoc.drop_pubmedDB()             
    
    def m102a_init_drop(self):
        ''' create a database in mysql
        in : configuration.cfg
        out : none
        '''
        logging.debug('m102a_init' )
        logging.debug(sys.path)
        myMedoc = MEDOC.MEDOC(self.cfg_file)

        # StepA : Create database if not exist
        myMedoc.create_pubmedDB()
        myMedoc.drop_pubmedDB()


    def m103a_in_name(self):
        ''' 
        i: 
        o: gz_file_list
        '''
        myMedoc = MEDOC.MEDOC(self.cfg_file)
        # Step B: get file list on NCBI
        gz_file_list = myMedoc.get_file_list()
        for file_to_download in gz_file_list:
            logging.info( file_to_download )
    
    def m104a_download(self):
        ''' actually download the medline file
        i:
        o:file_downloaded
        '''
        myMedoc = MEDOC.MEDOC(self.cfg_file)
        # Step B: get file list on NCBI
        gz_file_list = myMedoc.get_file_list()
        for file_to_download in gz_file_list:
            #print( file_to_download )
            file_downloaded = myMedoc.download(file_name=file_to_download)

    def m105a_extract(self):
        ''' extract file content
        i:
        o:file_downloaded
        '''
        myMedoc = MEDOC.MEDOC(self.cfg_file)        
        file_downloaded = self.file_downloaded_custom
        file_content = myMedoc.extract(file_name=file_downloaded)
        print(len(file_content))

    def m106a_parse(self):
        '''
        i:
        o: 
        '''
        myMedoc = MEDOC.MEDOC(self.cfg_file)
        file_downloaded = self.file_downloaded_custom
        file_content = myMedoc.extract(file_name=file_downloaded)
        # Step E: Parse XML file to extract articles
        articles = myMedoc.parse(data=file_content)

        articles_count = 0
        # Step F: Create a dictionary with data to INSERT for every article
        for raw_article in articles:

            #  Loading
            articles_count += 1
            if articles_count % 10000 == 0:
                print('{} articles inserted for file {}'.format(articles_count, file_downloaded))

        print(len(articles))

    def m107a_insert(self):
        '''
        '''
        myMedoc = MEDOC.MEDOC(self.cfg_file)
        file_downloaded = self.file_downloaded_custom
        file_content = myMedoc.extract(file_name=file_downloaded)
        # Step E: Parse XML file to extract articles
        articles = myMedoc.parse(data=file_content)

        articles_count = 0
        # Step F: Create a dictionary with data to INSERT for every article
        for raw_article in articles:

            #  Loading
            articles_count += 1
            if articles_count % 10000 == 0:
                print('{} articles inserted for file {}'.format(articles_count, file_downloaded))

            article_cleaned = re.sub('\'', ' ', str(raw_article))
            article_INSERT_list = myMedoc.get_command(article=article_cleaned, gz=file_downloaded)
            # print(article_INSERT_list);
            # Step G: For every table in articles, loop to create global insert
            for insert_table in article_INSERT_list:
                print( insert_table )

            break
        
    def m108a_getters(self):
        ''' get info from articles and set the row in the table
        i : parameters
        o : 
        '''
        # [] 
        parameters = configparser.ConfigParser()
        parameters.read(self.cfg_file)
        #logging.debug( parameters.sections() )        

        # [] 
        myMedoc = MEDOC.MEDOC(self.cfg_file)
        file_downloaded = self.file_downloaded_custom
        file_content = myMedoc.extract(file_name=file_downloaded)
        # Step E: Parse XML file to extract articles
        articles = myMedoc.parse(data=file_content)

        #  Lists to create
        values_tot_medline_citation = []

        articles_count = 0
        # Step F: Create a dictionary with data to INSERT for every article
        for raw_article in articles:

            #  Loading
            articles_count += 1
            if articles_count % 10000 == 0:
                print('{} articles inserted for file {}'.format(articles_count, file_downloaded))
            if ( len(values_tot_medline_citation) == self.insert_limit or (articles_count == self.insert_limit) ): 
                print('{} / {}'.format(articles_count, self.insert_limit))
                break


            article_cleaned = re.sub('\'', ' ', str(raw_article))
            article_INSERT_list = myMedoc.get_command(article=article_cleaned, gz=file_downloaded)
            #logging.info(article_INSERT_list);
            # Step G: For every table in articles, loop to create global insert
            for insert_table in article_INSERT_list:
                logging.debug( insert_table )
                #if ( len(values_tot_medline_citation) == self.insert_limit ): break

                #  ____ 1: medline_citation
                #if insert_table['name'] == 'medline_citation':
                #    values_medline_citation = getters.get_medline_citation(insert_table)
                    #logging.debug(values_medline_citation)
                #    values_tot_medline_citation.append('(' + ', '.join(values_medline_citation[0]) + ')')
                    #print( len(values_tot_medline_citation) == self.insert_limit )
                #    if (len(values_tot_medline_citation) == self.insert_limit) or (articles_count == len(articles)):
                #        getters.send_medline_citation(values_medline_citation[1], values_tot_medline_citation, parameters)
                #        values_tot_medline_citation = []
                #        break                       
        #pass

    def m109a(self):
        ''' get info from articles and set the row in the table
        i : parameters
        o : 
        '''


        #  Lists to create
        values_tot_medline_citation = []        
        articles_count = 0
        # Step F: Create a dictionary with data to INSERT for every article
        for raw_article in ['a','b','c']:

            #  Loading
            articles_count += 1
            logging.debug(articles_count)
            if articles_count % 10000 == 0:
                print('{} articles inserted for file {}'.format(articles_count, file_downloaded))
            if ( len(values_tot_medline_citation) == self.insert_limit or (articles_count == self.insert_limit) ): 
                continue        
        pass




def suite_a():
    suite = unittest.TestSuite()
    #suite.addTest(medoc1('m101a_cfg'))
    #suite.addTest(medoc1('m102a_init'))
    #suite.addTest(medoc1('m102a_init_drop'))    
    #suite.addTest(medoc1('m103a_in_name'))
    #suite.addTest(medoc1('m104a_download'))
    #suite.addTest(medoc1('m105a_extract'))
    #suite.addTest(medoc1('m106a_parse'))
    suite.addTest(medoc1('m107a_insert'))
    #suite.addTest(medoc1('m108a_getters'))
    #suite.addTest(medoc1('m109a'))
    return suite



if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite_a())

