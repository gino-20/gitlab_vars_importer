#!/usr/bin/python
import os
import argparse
def parse_env() -> dict:
    with open('.env', 'r') as env_file, open('.env.insert', 'w') as ins_file:
        # Parse .env to the var:value dict and make gitlab-ci script dummy
        t = ''
        result = {}
        while t:=env_file.readline():
            if not t[0].isupper():
                # Empty line or comments
                continue
            var = t.split('=')[0]
            val = t.split(t.split('=')[0])[1:]
            result.update({var:val})
            ins_str = '- echo '+var+'=${'+var+'} >> .env\n'
            ins_file.write(ins_str)
        # Done with parsing .env
    return result

def push_vars(gl_url: str, gl_user: str, gl_token: str, project_id, variables: dict) -> None:
    # push variables to the gitlab project
    curl_args = f' --header "PRIVATE-TOKEN: {gl_token}" "{gl_url}/api/v4/projects/{project_id}/variables/"'
    # First test the connection
    print(f'Going to push variables using the following address:\n{curl_args}')
    if os.system(f'curl -s {curl_args}>/dev/null'):
        print('Connection error, check parameters!')
        return
    print('Connection is OK, pushing variables!')
    for item in variables:
        print(f'Pushing {item}...')
        os.system(f'curl -s --request POST {curl_args} --form "key={item}" --form "value={variables[item]}"')
    print('Done!')    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Push local variables from .env file to the Gitlab hosted project',
                                    usage='Run with you Gitlab credentials')
    parser.add_argument('-url', type=str, help='Gitlab url (my.gitlab.com)')
    parser.add_argument('-user', type=str, help='Gitlab user')
    parser.add_argument('-token', type=str, help='Gitlab api token')
    parser.add_argument('-id', type=str, help='Gitlab project ID')
    args = parser.parse_args()
    parsed_vars=parse_env()
    push_vars(args.url,args.user,args.token,args.id,parsed_vars)
 
