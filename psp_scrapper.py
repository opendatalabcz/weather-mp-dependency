#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import csv

BASE_URL = "http://www.psp.cz/sqw/"

MONTHS_MAP = {
        'ledna' : '01',
        'února' : '02',
        'března' : '03',
        'dubna' : '04',
        'května' : '05',
        'června' : '06',
        'července' : '07',
        'srpna' : '08',
        'září' : '09',
        'října' : '10',
        'listopadu' : '11',
        'prosince' : '12'
};

def get_session_ids():
    """ Retrieves all available parliament sessions. """
    ids = [];
    
    response = requests.get( BASE_URL + "hlasovani.sqw?o=8" );
    content = BeautifulSoup( response.content, "html.parser", from_encoding="windows-1250" ).find( id='main-content' );
    
    data_table = content.find( 'table', attrs={ 'class' : 'approved-session-list' } );
    for session in data_table.tbody.find_all( 'tr' ):
        ids.append( int(session.td.find( 'a' ).get( 'href' )[13:]) );
        
    return ids;

def parse_date( date ):
    """ Converts textual date to list containing year, month number a day number."""
    date = date.split( '\xa0' );
    
    return [ date[ 2 ].strip(), MONTHS_MAP[ date[ 1 ].strip() ], int( float( date[ 0 ].strip() ) ) ];

def process_session( output_file_name, first_url ):
    """ Process single parliament session, i.e. reads all votings and store information about parliament member. """
    current_url = first_url;
    with open( output_file_name, 'a' ) as output_file:
        output_writer = csv.writer( output_file );
        next_voting = True

        while next_voting:
            next_voting = False
            print( '.', end='', flush=True )

            # Load page content.
            response = requests.get( BASE_URL + current_url );
            content = BeautifulSoup( response.content, "html.parser", from_encoding="windows-1250" ).find( id='main-content' );
            
            # Retrieves common info for this voting.
            voting_header = content.find( 'h1', attrs={'class' : 'page-title-x'} ).text.split( ',' );
            sess_no = voting_header[ 0 ].split( '.' )[ 0 ].strip();
            vot_no = voting_header[ 1 ].split( '.' )[ 0 ].strip();
            vot_date = parse_date( voting_header[ 2 ].strip() );
            vot_time = voting_header[ 3 ].lstrip()[:5].split( ':' );
        
            # Retrieves voting info for each parliament member.
            votings_per_party = content.find_all( 'ul', attrs={ 'class' : 'results' } );
            for voting in votings_per_party:
                personal_votings = voting.find_all( 'li' );
                for personal_voting in personal_votings:
                    row = [ personal_voting.a.text, personal_voting.span.text, sess_no, vot_no, vot_date[ 0 ], vot_date[ 1 ], vot_date[ 2 ], vot_time[ 0 ], vot_time[ 1 ] ];
                    output_writer.writerow( row );

            # Determines whether there is next voting in this session.
            next_link = content.find( 'a', attrs={ 'class' : 'next' } );
            if ( next_link != None ):
                next_voting = True;
                current_url = next_link.get( 'href' );

    output_file.close();

for session_id in get_session_ids():
    print( "Started " + str( session_id ) + ". session processing", end='', flush=True );
    response = requests.get( BASE_URL + 'phlasa.sqw?o=8&s=' + str( session_id ) + '&pg=1' );
    content = BeautifulSoup( response.content, "html.parser", from_encoding="windows-1250" ).find( id='main-content' );
    
    first_voting_link = content.find( 'table' ).find_all( 'tr' )[ 1 ].find_all( 'td' )[ 1 ].a.get( 'href' );
    
    process_session( 'psp_data.csv', first_voting_link );
    print( '\nDone!', flush=True )
