from rest_framework.test import APITestCase
from authentication.models import User             ##imports models to test

class TestModel(APITestCase):


#Test 1:CREATE USER:
    '''
    This test checks that a user created with appropriate fields is recognised as an instance of User.It also checks that the is_staff status is always false.
    '''
    def test_creates_user(self):
        user = User.objects.create_user('cryce', 'crycetruly@gmail.com', 'password123!@')                                              
        self.assertIsInstance(user,User)                                                              
        self .assertFalse(user.is_staff)                                                                
        self.assertEqual(user.email, 'crycetruly@gmail.com')                                           

#Test 2:CREATE SUPER-USER:
    '''
    This test checks that a superuser created with appropriate fields is recognised as an instance of User as well.It also checks that the is_staff status is always true since the superuser
    has is_staff status.
    '''
    def test_creates_super_user(self):
        user = User.objects.create_superuser('cryce', 'crycetruly@gmail.com', 'password123!@')                                              
        self.assertIsInstance(user,User)                                                               
        self.assertTrue(user.is_staff)                                                               
        self.assertEqual(user.email, 'crycetruly@gmail.com')                                           

#TEST 3: ABSENT USERNAME:
    '''
    This test ensures that the ValueError is raised when a username has not been given.
    '''
    def test_raises_error_when_username_is_not_supplied(self):
        self.assertRaises(ValueError,User.objects.create_user, username = '' ,email= 'crycetruly@gmail.com', password ='password123!@')   

#TEST 4: USERNAME-ERROR MESSAGE APPEARS:
    '''
    This test ensures that where an absent username occurs, the appropriate error message is shown. 
    '''   
    def test_raises_error_message_when_no_username_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given username must be set"):                                                 
            User.objects.create_superuser(username = '' ,email= 'crycetruly@gmail.com', password ='password123!@')   

#TEST 5: ABSENT EMAIL:
    '''
    This test ensures that the ValueError is raised when a email has not been given.
    '''
    def test_raises_error_when_email_is_not_supplied(self):
        self.assertRaises(ValueError,User.objects.create_user, username = 'cryce' ,email= '', password ='password123!@')      

#TEST 6: EMAIL-ERROR MESSAGE APPEARS:
    '''
    This test ensures that where an absent email occurs, the appropriate error message is shown. 
    ''' 
    def test_raises_error_message_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given email must be set"):                                                 
            User.objects.create_superuser(username = 'cryce' ,email= '', password ='password123!@') 
      
#TEST 7:SUPER USER IS_STAFF STATUS:  
    '''
    This test checks that a superuser is duly assigned a staff status.And if not, an error message is shown. 
    '''
    def test_creates_superuser_with_isstaff_status(self):
          with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):                                                 
            User.objects.create_superuser(username = 'cryce' ,email= 'crycetruly@gmail.com', password ='password123!@', is_staff= False)   

#TEST 8:SUPER USER IS_SUPERUSER STATUS:  
    '''
    This test checks that a superuser is duly assigned an superuser status.And if not, an error message is shown. 
    '''
    def test_creates_superuser_with_superuser_status(self):
          with self.assertRaisesMessage(ValueError, "Superuser must have is_superuser=True."):                                                 
            User.objects.create_superuser(username = 'cryce' ,email= 'crycetruly@gmail.com', password ='password123!@', is_superuser= False)   
 