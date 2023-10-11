import json_manager
import click

@click.group()
def cli():
     pass

# Creates a new user
@click.command(name = 'new', help = 'Creates a new user')
@click.option('--n', required = True, help = 'User name')
@click.option('--ln', required = True, help = 'User last name')
@click.pass_context
def new(ctx, n, ln):
     if not n or not ln:
          ctx.fail('Name and Lastname are required')
     else:
          data = json_manager.read_json()
          new_id = len(data) + 1
          new_user = {
               'id': new_id,
               'name': n,
               'lastname': ln
          }
          data.append(new_user)
          json_manager.write_json(data)        

# Shows all users
@click.command(help = 'Shows all users')
def users():
     users = json_manager.read_json()
     for user in users:
          print("{")
          print(f'    id: {user["id"]},')
          print(f'    name: {user["name"]},')
          print(f'    lastname: {user["lastname"]}')
          print("}")

# Finds user by ID
@click.command(help = 'Finds user by id')
@click.argument('id', type = int)
def user_find(id):
     data = json_manager.read_json()
     user = next((x for x in data if x['id'] == id), None)
     if user is None:
          print(f'User with id "{id}" not found')
     else:
          print("{")
          print(f'    id: {user["id"]},')
          print(f'    name: {user["name"]},')
          print(f'    lastname: {user["lastname"]}')
          print("}")

# Deletes user by ID
@click.command(help = 'Deletes user by id')
@click.argument('id', type = int)
def delete(id):
     data = json_manager.read_json()
     user = next((x for x in data if x['id'] == id), None)
     if user is None:
          print(f'User with id "{id}" not found')
     else:
          data.remove(user)
          json_manager.write_json(data)
          print(f'User with id "{id}" deleted successfully')

# Change a user name or last name
@cli.command(help = 'Change user name or user last name')
@click.argument('id', type = int)
@click.option('--n', help = 'User name')
@click.option('--ln', help = 'User last name')
def update(id, n, ln):
     data = json_manager.read_json()
     for user in data: 
          if user['id'] == id:
               if n is not None:
                    user['name'] = n
               if ln is not None:
                    user['lastname'] = ln
               break
     json_manager.write_json(data)
     print(f'User with id "{id}" updated successfully')

cli.add_command(users)
cli.add_command(new)
cli.add_command(user_find)
cli.add_command(delete)
if __name__ == '__main__':
     cli()