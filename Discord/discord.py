from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


class ServerNotPresentException(Exception):
    """Raise if requested server is not present"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "ServerNotPresentException: {}".format(self.name)


class ChannelNotPresentException(Exception):
    """Raise if requested channel is not present"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "ChannelNotPresentException: {}".format(self.name)


class MessageNotFoundException(Exception):
    """Raise if requested message is not found"""

    def __init__(self, contents):
        self.contents = contents

    def __str__(self):
        return "MessageNotFoundException: {}".format(self.contents)


class DiscordConfiguration():
    """Contains configuration options for 'DiscordHome' objects"""

    def __init__(self, timeout=5, target_server=None, target_channel=None):
        """Contains all DiscordHome configuration settings"""
        self.timeout = timeout
        self.target_server = target_server
        self.target_channel = target_channel

    def __str__(self):
        return "DiscordConfiguration:\n\tTimeout:\t{}\n\tTarget Server:\t{}\n\tTarget Channel:\t{}".format(self.timeout, self.target_server, self.target_channel)


class DiscordHome():
    """Contains all enumerated Discord objects"""

    def __init__(self, driver: webdriver, config=DiscordConfiguration()):
        self.driver = driver
        self.config = config
        WebDriverWait(driver, self.config.timeout).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[aria-label='Servers']")))
        self.numservers = 0
        if self.config.target_server is None:
            self.servers = self.get_servers()
        else:
            self.target_server = self.get_target_server()

    def __str__(self):
        return "Discord Home:\n\tServers:\t{}".format(self.name, self.numservers)

    def get_servers(self):
        """Enumerates all servers in DiscordHome"""
        servers = []
        servlist = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Servers']").find_elements(
            By.CSS_SELECTOR, "[class='listItem-3SmSlK']")
        for server in servlist:
            newserver = DiscordServer(self, server)
            servers.append(newserver)
            self.numservers += 1
        return servers

    def get_target_server(self):
        """Finds target server and navigatest to it if found"""
        servlist = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Servers']").find_elements(
            By.CSS_SELECTOR, "[class='listItem-3SmSlK']")
        for server in servlist:
            try:
                newserver = DiscordServer(self, server)
                if newserver.name == self.config.target_server:
                    self.numservers += 1
                    newserver.server.click()
                    return newserver
            except ChannelNotPresentException as e:
                if server == servlist[-1]:
                    raise e
        raise ServerNotPresentException(self.config.target_server)

    def get_server_by_name(self, name):
        """Retrieve server element by name"""
        for server in self.servers:
            if (server.name == name):
                return server
        raise ServerNotPresentException(name)

    def goto_server_by_name(self, name):
        """Navigates to server based on name"""
        for server in self.servers:
            if (server.name == name):
                server.server.click()
                return server
        raise ServerNotPresentException(name)


class DiscordServer():
    """Holds home's channels as 'DiscordChannel' objects"""

    def __init__(self, home: DiscordHome, server):
        self.server = server
        self.server.click()
        WebDriverWait(home.driver, home.config.timeout).until(EC.presence_of_element_located(
            (By.ID, 'channels')))
        self.home = home
        self.name = self.home.driver.find_element(
            By.CSS_SELECTOR, '[class="name-3Uvkvr"]').text
        if self.home.config.target_channel is None:
            self.text_channels = self.get_channels()
        else:
            self.target_channel = self.get_target_channel()

    def get_channels(self):
        """Fully enumerates text channels in DiscordServer"""
        WebDriverWait(self.home.driver, self.home.config.timeout).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[aria-label="Channels"]')))
        textchanlist = self.home.driver.find_elements(
            By.CSS_SELECTOR, '[aria-label="Text"]')
        self.numchannels = 0
        text_channels = []
        for channel in textchanlist:
            newchannel = DiscordTextChannel(self, self.home, channel)
            text_channels.append(newchannel)
            self.numchannels += 1
        return text_channels

    def get_target_channel(self):
        """Searches for specific channel in DiscordServer and navigates to it if found"""
        WebDriverWait(self.home.driver, self.home.config.timeout).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[aria-label="Channels"]')))
        textchanlist = self.home.driver.find_elements(
            By.CSS_SELECTOR, '[aria-label="Text"]')
        self.numchannels = 0
        target_channel = None
        for channel in textchanlist:
            newchannel = DiscordTextChannel(self, self.home, channel)
            if newchannel.name == self.home.config.target_channel:
                target_channel = newchannel
                self.numchannels += 1
                target_channel.channel.click()
                return target_channel
        raise ChannelNotPresentException(self.home.config.target_channel)

    def get_text_channel_by_name(self, name):
        """Retrieve server element by name"""
        for channel in self.text_channels:
            if (channel.name == name):
                return channel
        raise ChannelNotPresentException(name)

    def goto_text_channel_by_name(self, name):
        """Navigates to server based on name"""
        for channel in self.text_channels:
            if (channel.name == name):
                channel.channel.click()
                return channel
        raise ChannelNotPresentException(name)

    def __str__(self):
        if self.home.config.target_channel is None:
            return "Discord Server:\n\tName:\t{}\n\tChannels:\t{}".format(self.name, self.numchannels)
        else:
            return "Discord Server:\n\tName:\t{}\n\tTarget Channel:\t{}".format(self.name, self.target_channel)


class DiscordTextChannel():
    """Holds home's channels as 'DiscordChannel' objects"""

    def __init__(self, server: DiscordServer, home: DiscordHome, channel):
        self.channel = channel
        self.channel.click()
        WebDriverWait(home.driver, home.config.timeout).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[aria-label="Channel header"]')))
        self.name = home.driver.find_element(
            By.CSS_SELECTOR, '[class*="title-17SveM"]').text
        self.server = server
        self.home = home

    def __str__(self):
        return "Text Channel:\n\tName:\t{}".format(self.name)

    def refresh(self):
        """Refreshes self.channel element to prevent stale element exception"""
        self.channel = self.home.driver.find_element(
            By.CSS_SELECTOR, '[data-dnd-name="{}"]'.format(self.name))

    def get_messages(self):
        """Gets messages in channel"""
        self.refresh()
        self.channel.click()
        msglist = self.home.driver.find_elements(
            By.CSS_SELECTOR, '[aria-roledescription="Message"]')
        self.messages = []
        for msg in msglist:
            self.messages.append(DiscordMessage(self, self.home, msg))

    def get_messages_by_contents(self, msgtext, partials_allowed=False):
        """Returns all messages with contents matching msgtext (NON CASE SENSITIVE)"""
        self.refresh()
        matchlist = []
        self.get_messages()
        for message in self.messages:
            if partials_allowed:
                if msgtext.lower() in message.content.lower():
                    matchlist.append(message)
            else:
                if msgtext.lower() == message.content.lower():
                    matchlist.append(message)
        return matchlist

    def post(self, post):
        """Posts message to channel"""
        self.refresh()
        self.channel.click()
        textbox = self.home.driver.find_element(
            By.CSS_SELECTOR, '[role="textbox"]')
        textbox.click()
        actions = ActionChains(self.home.driver)
        actions.send_keys("{}\n".format(post)).perform()


class DiscordMessage():
    """Holds message attributes"""

    def __init__(self, channel: DiscordTextChannel, home: DiscordHome, message):
        """Extracts message elements"""
        self.home = home
        WebDriverWait(home.driver, home.config.timeout)\
            .until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                   '[id*="chat-messages"]')))
        self.message = message
        contents = self.message.find_element(
            By.CSS_SELECTOR, '[class*="contents"]')
        self.sender = None
        self.channel = channel

        try:
            header = contents.find_element(
                By.CSS_SELECTOR, '[class="header-2jRmjb"]')
            self.sender = header.find_element(
                By.CSS_SELECTOR, '[id*="message-username"]').text
            self.content = header.find_element(
                By.CSS_SELECTOR, '[id*="message-content"]').text
            raw_timestamp = header.find_element(
                By.CSS_SELECTOR, '[class*="timestamp"]').get_attribute('datetime')

        except:
            self.content = contents.find_element(
                By.CSS_SELECTOR, '[id*="message-content"]').text
            raw_timestamp = contents.find_element(By.CSS_SELECTOR, '[class*="timestamp"]').find_element(
                By.CSS_SELECTOR, '[id*="timestamp"]').get_attribute('datetime')

        self.timestamp = datetime.strptime(
            raw_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

    def reply(self, replymsg: str):
        action = ActionChains(self.home.driver)
        action.context_click(self.message).perform()
        WebDriverWait(self.home.driver, self.home.config.timeout)\
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "[id='message-reply']")))
        reply_button = self.home.driver.find_element(
            By.CSS_SELECTOR, "[id='message-reply']")
        reply_button.click()
        action.send_keys("{}\n".format(replymsg)).perform()

    def delete(self):
        """Deletes message"""
        action = ActionChains(self.home.driver)
        action.context_click(self.message).perform()
        WebDriverWait(self.home.driver, self.home.config.timeout)\
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "[id='message-delete']")))
        delete_button = self.home.driver.find_element(
            By.CSS_SELECTOR, "[id='message-delete']")
        action.key_down(Keys.SHIFT).click(
            delete_button).key_up(Keys.SHIFT).perform()

    def __str__(self):
        return "\tSender:\t\t{}\n\tTimestamp:\t{}\n\tContent:\t{}".format(self.sender, self.timestamp, self.content)
