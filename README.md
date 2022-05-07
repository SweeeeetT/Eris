# Eris
## Simple Python API for user account automation with Discord web-client
- Allows user account automation without being labeled as a bot
- Supports basic functionality, but is still a work-in-progress

## Dependencies:
- Selenium -- `pip3 install selenium`
- WebDriver (RealBot was tested with Chrome)
- Chrome Driver -- Installation Instructions Can Be Found At:
    - Ubuntu: https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/
    - Windows: https://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-windows-install/

## Notes and Limitations:
- If your code uses the API to change the contents of a server (i.e. posting a message, deleting a message, replying to a message, etc.) you will need to allow time for that change to be posted based on your machine and internet speed, before you continue to try to interact with the web client.

## Roadmap:
- Support private channels
- Support DM automation
- Extend similar functionality to Slack web client
