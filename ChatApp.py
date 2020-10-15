#####################################################
import time
from os.path import exists as path_ok
#Application gestures:
backup_succeeded = 'Data was backed up successfully to:\n'
backup_failed = 'Failed to backup you data. Please try again later.\n'
sending_succeeded_msg = 'Message was sent successfully!\n'
removing_succeeded_msg = 'Message was removed successfully!\n'
empty_conversation = 'Conversation either didn\'t start or all messages were removed.\n'
no_permissions_msg = 'Sorry! you are not a member of this conversation.\n'
no_such_msg = 'Message does not exist.\n'
thanks_msg = '\nThank you for using ChatApp! See you soon. Bye.\n'
#####################################################


class Date:
    
    def __init__(self, current_time):
        current_time = current_time.split(',')
        self.hour=str(current_time[0])
        self.minute=str(current_time[1] )
        self.second=str( current_time[2])

    def __str__(self):           
        return self.hour + ":" + self.minute + ":" + self.second



class Message:
    
    def __init__(self, sender, content, date, msg_id):
        self.sender = sender
        self.content = content
        self.date = date
        self.id = msg_id
        

    def __len__(self):
        return len(self.content)
        
    def __str__(self):
       return "(" + str(self.id) + ") " + str(self.date) + " " + self.sender + ": " + self.content


    
class Conversation:
    
    def __init__(self, members, size_limit, backup_policy, cloud_account_prefix='./'):
        self.is_valid(members, size_limit, backup_policy, cloud_account_prefix)
        self.members = members
        self.size_limit = size_limit
        self.backup_policy = backup_policy
        self.cloud_account =cloud_account_prefix + members[0] + ".txt"
        self.size = 0
        self.total_messages_sent = 0
        self.content = []
        
       
    def __len__(self):
        return self.total_messages_sent

    def __str__(self):
        convers=''
        for message in self.content:
            convers+=str(message)+'\n'
        convers=convers[:-1]
        return convers
           
        
    def is_valid(self, members, size_limit, backup_policy, cloud_account_prefix):
        if len(members) < 2 or size_limit <= 10 or  backup_policy < 1 or not path_ok(cloud_account_prefix):
            raise ValueError
        
        else:

            return None
    
    def is_member(self, username):
        for member in self.members:
            if username == member:
                return True
        
        return False
            
    
    def enough_space(self, msg):
        if len(msg) + self.size <= self.size_limit:
            return True
        else:
            return False
        
    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False
        
    def time_for_backup(self):
        if self.total_messages_sent % self.backup_policy == 0:

            return True
        else:
            return False
        
    def backup_content(self):
        global backup_failed, backup_succeeded
        if self.time_for_backup() == True:
            try:
                f = open(self.cloud_account, 'w')
                for line in range(len(self.content)-1):
                    f.write(str(self.content[line]) + "\n")
                f.write(str(self.content[-1]))
                f.close()
                print(backup_succeeded + self.cloud_account)
            except IOError:
                print(backup_failed)
                

    def get_conversation(self):
        global empty_conversation
        
        if self.is_empty()== False:
            return str(self)
        else:
            return empty_conversation
      
    def send_msg(self, username, msg_content, msg_time):
        global sending_succeeded_msg
        message_cur = Message(username, msg_content, msg_time, self.total_messages_sent + 1)
        if not self.enough_space(message_cur):
            raise MemoryError
        else:
            self.total_messages_sent += 1
            self.content.append(message_cur)
            self.backup_content()
            self.size += len(message_cur)
            return sending_succeeded_msg
            
    def find_msg_index(self, msg_id): 
        for i in range(len(self.content)):
            if msg_id == self.content[i].id:
                return i
        else:
            return -1
            
   
    def delete_msg(self, msg_id_str):
        global removing_succeeded_msg
        msg_id_int = int(msg_id_str)
        if self.find_msg_index(msg_id_int) == -1:
            raise ValueError
        else:
            self.size -= len(self.content[self.find_msg_index(msg_id_int)])
            self.content.remove(self.content[self.find_msg_index(msg_id_int)])
            return removing_succeeded_msg
            

#####################################################
        
class Application:
    
    def __init__(self):
        '''
        Initializes the app. Think about it as an "installation".
        '''
        conversation_parameters = self.get_conversation_parameters_from_user()
        self.coversation = Conversation(*conversation_parameters)

        
    def get_conversation_parameters_from_user(self):
        '''
        Ask the user for parameters once as part of a conversation initialization.
        '''
        num_of_members = int(raw_input('Please enter the number of members in the group.\n'))
        members = []
        for i in range(num_of_members):
            members.append(raw_input('Please enter member number '+ str(i+1) +':\n'))
        size_limit = int(raw_input('Please enter your storage limit (int):\n'))
        backup_policy = int(raw_input('Please a desired backup policy (int):\n'))
        path = raw_input('Please enter a file path for backing up your data:\n')
        return members, size_limit, backup_policy, path.rstrip('/') + '/'
        
    def show_options(self):
        '''
        Prints the available options to the user. Nothing is returned.
        '''
        print('\n' + '#'*50 + '''\nWelcome to ChatApp! What would you like to do?)
        [0] End conversation
        [1] Show full conversation
        [2] Send new message
        [3] Remove existing message\n'''
    
    
    def get_user_choice(self):
        '''
        Gets user's input for the expected operation and returns the choice number 
        if it is valid; -1 otherwise.
        '''    
        illegal_choice_msg = 'Choice is illegal. Please pick a number between 0 and 3'
        user_input = raw_input('Please type your choice and press ENTER\n')
        try:
            choice = int(user_input)
            if (0 <= choice <= 3):
                return choice
        except ValueError:
            print(illegal_choice_msg)
        return -1
            
    def run(self):
        '''
        Runs an "infinite" dialog loop and executes users requests. Nothing is 
        returned.
        '''
        global no_permissions_msg, no_such_msg, thanks_msg
        while True:
            time.sleep(1.5)
            self.show_options()
            choice = self.get_user_choice()
            if choice == -1:
                continue
            elif choice == 0:
                print(thanks_msg)
                break
            else:
                username = raw_input('Please enter username (only conversation\'s members are allowed to send/read messages).\n')
                if not self.coversation.is_member(username):
                    print(no_permissions_msg)
                    continue
                if choice == 1:
                    response = self.coversation.get_conversation()
                    print(response)
                elif choice == 2:
                    msg_content = raw_input('Please type your message.\n')
                    msg_time = Date(time.strftime('%H,%M,%S'))
                    response = self.coversation.send_msg(username, msg_content, msg_time)
                    print(response)
                elif choice == 3:
                    msg_id_str = raw_input('Please enter message id.\n')
                    try:
                        response = self.coversation.delete_msg(msg_id_str)
                    except ValueError:
                        response = no_such_msg
                    print(response)


########################################################
#     Optional: Paste the content of Tests.py below    #

########################################################

''' Main code. Do not change!'''
try:
    app = Application()
    app.run()
except ValueError:
    print('\nOne (or more) of the parameter values is illegal.')
    time.sleep(1)
    print('\nFailed to initialize the app.')
    time.sleep(1)
    print('\nExiting',)
    for i in range(3):
        time.sleep(0.5)
        print('.',)
    time.sleep(0.5)
    print('\n')

    
   
        
        
    
    
