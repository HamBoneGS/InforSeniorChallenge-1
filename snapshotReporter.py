##
# @author Graham Schmidt
# Purpose: To pull two reports on current ec2 Instance snapshots
##
from classes import SnapshotUtility

# I assume I shouldn't give y'all my actual keys
ACCESSKEY = "ABCD"
SECRETKEY = "EFG"

# Initialize snapshot utility
su = SnapshotUtility()

# Pull appropriate data
snapData = su.pull_data(ACCESSKEY, SECRETKEY)

# Generate file #1, 'details'
su.generate_long_report(snapData)

# Generate file #2, 'tags'
su.generate_short_report(snapData)
