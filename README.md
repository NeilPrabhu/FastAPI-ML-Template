# Lab 4

### example curl request
To Test this application, you can run the following curl request"
curl -s -X POST "https://neilprabhu.mids255.com/predict" -H 'Content-Type: application/json' -d '{"houses" : [{"income":12000.0,"house_age":20.2,"avg_room":2.3,"avg_bedroom":3,"avg_occup":4,"lattitude":12.29,"longitude":37.82,"population":100000},{"income":12000.0,"house_age":20.2,"avg_room":2.3,"avg_bedroom":3,"avg_occup":4,"lattitude":12.29,"longitude":37.82,"population":100000}]}'


### Questions

#### What are the downsides of using latest as your docker image tag?
If you use latest as docker image tag it can cause issues distinguishing if your image with tag "latest" is actually the latest. By using the
the short hash of last git commit can help distinguish which version of the repository is running on K8s. The tag "latest" can also just cause confusion and lead to harder time debugging.

#### What does kustomize do for us?
Kustomize allows us to edit our original templates without actually modifying them. This helps us so we don't require multiple copies for different environments (i.e. prod, testing, dev).
