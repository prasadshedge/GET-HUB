#!/usr/bin/env python
# coding: utf-8

# In[ ]:


Write an efficient algorithm to check if a string is a palindrome. A string is a
  palindrome if the string matches the reverse of string.
  Example: 1221 is a palindrome but not 1121.


# In[ ]:





# In[4]:


def check_palindrome_1(string):
    reversed_string = string[::-1]
    status=1
    if(string!=reversed_string):
        status=0
    return status
string = input("Enter the string: ")
status= check_palindrome_1(string)
if(status):
    print("It is a palindrome ")
else:
    print("Sorry! Try again")
    


# In[ ]:


Using Reverse Function


# In[5]:


def check_palindrome_1(string):
    reversed_string = string[::-1]
    status=1
    if(string!=reversed_string):
        status=0
    return status
string = input("Enter the string: ")
status= check_palindrome_1(string)
if(status):
    print("It is a palindrome ")
else:
    print("Sorry! Try again")


# In[ ]:




