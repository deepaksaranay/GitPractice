# DevOps Engineer Roadmap (Step by Step)

इस रिपॉजिटरी में मैं DevOps सीखते हुए अपनी प्रोग्रेस, नोट्स और प्रोजेक्ट्स अपलोड करूँगा।

> नियम: हर टॉपिक के बाद एक छोटा प्रोजेक्ट बनाओ और उसे इसी repo में commit करो।

## Phase 0 – Basics (2-3 हफ्ते)
- [ ] Computer Networking: IP, DNS, HTTP/HTTPS, TCP/UDP, ports, firewall, load balancer
- [ ] Operating System: processes, memory, file system, permissions
- [ ] Programming की समझ (Python या Go)
- **प्रोजेक्ट:** एक छोटा Python script जो server का disk/CPU usage दिखाए

## Phase 1 – Linux & Shell Scripting (3-4 हफ्ते)
- [ ] Linux commands: `ls cd cp mv rm grep find awk sed curl ssh`
- [ ] User/Group, file permissions (`chmod`, `chown`), `systemctl`, `cron`
- [ ] Bash scripting: variables, loops, functions
- **प्रोजेक्ट:** Backup script जो folder को zip करके दूसरी जगह कॉपी करे और cron से रोज चले

## Phase 2 – Git & GitHub (2 हफ्ते)
- [ ] `init clone add commit push pull`
- [ ] Branching, merge, rebase, conflict resolve
- [ ] Pull Request, Code Review, `.gitignore`
- [ ] GitHub Flow / Git Flow
- **प्रोजेक्ट:** इसी repo में रोज़ commit करो और एक PR बनाकर merge करो

## Phase 3 – Cloud (AWS / Azure / GCP में से कोई एक) (4-6 हफ्ते)
- [ ] IAM, EC2/VM, S3/Storage, VPC, Security Groups
- [ ] Load Balancer, Auto Scaling, RDS, Route53
- [ ] Monitoring: CloudWatch
- **प्रोजेक्ट:** VPC के अंदर EC2 पर एक web app deploy करो

## Phase 4 – CI/CD (3-4 हफ्ते)
- [ ] GitHub Actions (शुरुआत यहीं से), फिर Jenkins / GitLab CI
- [ ] Build → Test → Deploy pipeline
- [ ] Secrets management
- **प्रोजेक्ट:** हर push पर tests चलें और app अपने आप deploy हो

## Phase 5 – Containers: Docker (3 हफ्ते)
- [ ] Image, Container, Dockerfile, multi-stage build
- [ ] Docker Compose, volumes, networks
- [ ] Docker Hub / ECR registry
- **प्रोजेक्ट:** अपनी app को dockerize करके Docker Hub पर push करो

## Phase 6 – Kubernetes (5-6 हफ्ते)
- [ ] Pod, Deployment, Service, Ingress, ConfigMap, Secret
- [ ] Volumes (PV/PVC), Namespaces, RBAC
- [ ] Helm, HPA (autoscaling)
- [ ] Minikube / kind पर practice, फिर EKS/AKS/GKE
- **प्रोजेक्ट:** 3-tier app को Kubernetes पर deploy करो

## Phase 7 – Infrastructure as Code (4 हफ्ते)
- [ ] Terraform: providers, state, modules, workspaces
- [ ] Ansible: inventory, playbooks, roles
- **प्रोजेक्ट:** Terraform से पूरा AWS infra बनाओ और Ansible से server configure करो

## Phase 8 – Monitoring & Logging (3 हफ्ते)
- [ ] Prometheus + Grafana (metrics, dashboards, alerts)
- [ ] ELK / EFK stack या Loki (logs)
- **प्रोजेक्ट:** अपनी app का Grafana dashboard और alert बनाओ

## Phase 9 – Security / DevSecOps (2-3 हफ्ते)
- [ ] Secrets (Vault, AWS Secrets Manager)
- [ ] Image scanning (Trivy), SAST (SonarQube)
- [ ] Least privilege, SSL/TLS

## Phase 10 – GitOps & Advanced (ongoing)
- [ ] ArgoCD / Flux
- [ ] Service Mesh (Istio), SRE concepts (SLI/SLO/SLA)
- [ ] Cost optimization, Disaster Recovery

## Final Capstone Project
**End-to-end pipeline:** Code push → GitHub Actions (build/test/scan) → Docker image → Registry → Terraform से infra → Kubernetes पर ArgoCD से deploy → Prometheus/Grafana monitoring

## Certifications (optional)
- AWS Cloud Practitioner → AWS Solutions Architect Associate
- CKA (Kubernetes), Terraform Associate

## Progress Log
| Date | Topic | Done |
|------|-------|------|
|      |       |      |
