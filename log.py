import logging

# Configure logging for authLog.txt
authLog = logging.getLogger('authLog')
authLog.setLevel(logging.DEBUG)
authHangler = logging.FileHandler('authLog.txt')
authHangler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
authLog.addHandler(authHangler)

# Configure logging for configChangesLog.txt
configChangeLog = logging.getLogger('configChangeLog')
configChangeLog.setLevel(logging.INFO)
configHandler = logging.FileHandler('configChangesLog.txt')
configHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
configChangeLog.addHandler(configHandler)

# Configure logging for invalidIPLog.txt
invalidIPLog = logging.getLogger('invalidIPLog')
invalidIPLog.setLevel(logging.INFO)
invalidIPHandler = logging.FileHandler('invalidIPLog.txt')
invalidIPHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
invalidIPLog.addHandler(invalidIPHandler)

# Configure Logging for Netmiko
# No longer needed !!!!!
# netmikoLogger = logging.getLogger("netmiko")
# netmikoLogger.setLevel(logging.DEBUG)
# netmikoHandler = logging.FileHandler('netmikoLog.txt')
# netmikoHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# netmikoLogger.addHandler(netmikoHandler)

# Usage Example
# authLog.info('This is a message for auth_log.txt')
# configChangeLog.info('This is a message for config_Changes_Log.txt')
