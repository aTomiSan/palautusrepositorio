*** Settings ***
Resource  resource.robot 
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  kallo
    Set password  kallo666 
    Confirm password  kallo666 
    Click Register 
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  k
    Set password  kallo666 
    Confirm password  kallo666 
    Click Register 
    Register Should Fail With Message  Invalid username: minimum of 3 a-z characters

Register With Valid Username And Too Short Password
    Set Username  kallo
    Set password  k666 
    Confirm password  k666 
    Click Register 
    Register Should Fail With Message  Invalid password: minimum length 8

Register With Valid Username And Invalid Password
    Set Username  kallo
    Set password  kallokallo 
    Confirm password  kallokallo
    Click Register 
    Register Should Fail With Message  Invalid password: not only characters

Register With Nonmatching Password And Password Confirmation
    Set Username  kallo
    Set password  kallo666 
    Confirm password  kallo669 
    Click Register 
    Register Should Fail With Message  Invalid password: passwords do not match

Register With Username That Is Already In Use
    Set Username  kalle
    Set password  kalle123
    Confirm password  kalle123 
    Click Register 
    Register Should Fail With Message  User with username kalle already exists

Login After Successful Registration
    Set Username  kallo
    Set password  kallo666 
    Confirm password  kallo666 
    Click Register 
    Register Should Succeed
    Click Link  Continue to main page
    Click Button  Logout
    Go To Login Page 
    Set Username  kallo
    Set Password  kallo666
    Submit Credentials
    Login Should Succeed

Login After Failed Registration
    Set Username  k
    Set password  kallo666 
    Confirm password  kallo666 
    Click Register 
    Click Link  Login
    Set Username  k
    Set Password  kallo666
    Submit Credentials
    Login Should Fail With Message  Invalid username or password


*** Keywords ***
Set Username 
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Confirm Password
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

Click Register 
    Click Button  Register

Register Should Succeed 
    Welcome Page Should Be Open

Register Should Fail With Message 
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}


*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page
