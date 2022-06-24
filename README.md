![](app/static/images/inventorius.png)
# INVENTORIUS
Inventorius is a internal infrastructure monitoring tool for large distributed environments.

####Have an ability to

- Scan IPs for subnets
- Seperate them to different views

#### Features
- Getting Clusters General Info (Kubernetes, Kafka)
- Vsphere size information
- Watching Applications Availability
- Alarm mechanism for cronicle problems

## Installation
 - Python 3.7+
 - Django
 - Celery
 - Redis
 - Nmap
 - Nginx
 
        git clone https://github.com/erkanderon/inventorius.git
		pip install -r requirement.txt
		
		Make sure nmap binary is in PATH
		
		Configure app/settings.py to installed redis url
		
		start_celery_worker.sh
		start_celery_beat.sh
		start_app.sh

		Configure NGINX with example conf to serve site.


### TODO LIST v2.0.0

- [x] v1.0.0 review
- [x] commons seperation
- [x] environments page organization
- [x] environments page add and remove
- [x] environments page edit
- [x] environments page details
- [x] ip - subnet manytomany relationship
- [x] Regex form add or remove
- [ ] Simple machine app status check with celery

### TODO LIST v3.0.0

- [x] v2.0.0 review
- [ ] monitoring spesific host and port
- [ ] alarm graphical representation
- [ ] alarm when you took thresholded failure

### TODO LIST v4.0.0

- [x] v3.0.0 review
- [ ] kafka monitoring
- [ ] couchbase monitoring
- [ ] vm connector for general monitoring


### BUGFIX v1.0.0

- [x] False when dns is empty
- [x] always creating new ip
- [x] analyzing some known ports