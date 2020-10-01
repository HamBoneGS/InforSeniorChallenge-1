##
# @author Graham Schmidt
# Purpose: To pull two reports on current ec2 Instance snapshots
##
from classes import SnapshotUtility

# I assume I shouldn't give y'all my actual keys
ACCESSKEY = "AKIASEE3GL7WKECBOP7D"
SECRETKEY = "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"

# Initialize snapshot utility
su = SnapshotUtility()

# Pull appropriate data
snapData = su.pull_data(ACCESSKEY, SECRETKEY)

# Generate file #1, 'details'
su.generate_long_report(snapData)

# Generate file #2, 'tags'
su.generate_short_report(snapData)
