import boto3, csv, datetime

class SnapshotUtility:
    def __init__(self):
        pass


    def pull_data(self, ACCESSKEY, SECRETKEY):
        ec2 = boto3.client('ec2', aws_access_key_id=ACCESSKEY, aws_secret_access_key=SECRETKEY)
        regions = ec2.describe_regions()
        regionDictList = regions['Regions']
        print("## Regions accessed")
        regionList = []
        for dict in regionDictList:
            regionList.append(dict['RegionName'])
        print("## Region list built")

        snapData = []
        for r in regionList:
            # Create ec2 Resource and Instances
            print("## Creating Resource Object...")
            ec2 = boto3.resource('ec2', region_name=r)
            print("## Resource Object Created")
            print("## Building Instances List...")
            instances = ec2.instances.filter()
            print("## Instances List Built")

            # Iterate over instances, pull Snapshot data into snapData (list) as a dict
            print("## Iterating over instances...\n")
            for instance in instances:
                i = ec2.Instance(instance.id)
                volume_iterator = i.volumes.all()
                for v in volume_iterator:
                    snapshot_iterator = v.snapshots.all()
                    print("\n## Retrieving Snapshot Data\n")
                    for s in snapshot_iterator:
                        data = {'Region': r, 'ID': s.snapshot_id, 'Size': str(s.volume_size) + "GiB", 'Created_Date': s.start_time.strftime("%Y-%m-%d_%H:%M:%S"), 'Tags': s.tags}
                        snapData.append(data)
        return snapData

    def generate_long_report(self, snapData):
        # Generate file names
        now = datetime.datetime.now()
        dt = now.strftime("%Y-%m-%d_%H-%M-%S")
        logname = "details_log{}.csv".format(dt)

        print("\n## Generating Report #1")
        with open(logname, 'w', newline='') as csvfile:
            fieldnames = ['Region', 'ID', 'Size', 'Created_Date']
            datawriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            datawriter.writeheader()
            for dict in snapData:
                datawriter.writerow({'Region':dict['Region'], 'ID':dict['ID'], 'Size':dict['Size'], 'Created_Date':dict['Created_Date']})

    def generate_short_report(self, snapData):
        # Generate file names
        now = datetime.datetime.now()
        dt = now.strftime("%Y-%m-%d_%H-%M-%S")
        logname2 = "tags_log{}.csv".format(dt)

        # Generate file #2, 'tags'
        print()
        print("## Generating Report #2")
        with open(logname2, 'w', newline='') as csvfile2:
            fieldnames = ['ID', 'Tags']
            datawriter = csv.DictWriter(csvfile2, fieldnames=fieldnames)
            datawriter.writeheader()
            for dict in snapData:
                datawriter.writerow({'ID':dict['ID'], 'Tags':dict['Tags']})
