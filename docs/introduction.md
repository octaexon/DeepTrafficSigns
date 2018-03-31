### Links
[home](../README.md) &#8226; [intro](introduction.md) &#8226; [env](environment.md)

### Introduction

Well, let's get the ball rolling by first attempting to understand more precisely what I would
actually like to do. 

#### Task

At the outset, the task is to develop a product that ingests a live camera feed, comprehends road
signs and alerts the driver.

#### Constraints

Of course, the precise form of the ultimate product is heavily determined by the many and various
constraints that come into play.

- **time** I have roughly 2-3 weeks to learn the necessary tools, develop the system, provide the
  content for this associated website and hone a 10 minute presentation. Obviously, the first two
  points are the immediate priorities but in any case, time is at a premium here.

- **computational capacity during development** I should anticipate that training a neural network
  for object detection is a computationally intensive task. While moving to the cloud for better
  hardware is a feasible (and in most cases necessary) option, it is not a panacea for all ills.
  Indeed, the received wisdom is that training a viable detection network *from scratch* requires much
  more computational capacity, time (and data!) than I have at my disposal. I'm going to have to
  devise/find an alternative strategy.

- **data availability** I'm living in Berlin and thankfully there is a readily available dataset,
  the venerable [GTSDB](http://benchmark.ini.rub.de/?section=gtsdb) (German Traffic Sign Detection
  Benchmark). Having said that, it is not a large dataset, and the frequency of any given sign 
  is quite small.  As a result, I should budget some time for data collection, labelling and
  extra preprocessing.

- **computational capacity in production** I want to deploy my model on a raspberry pi with camera
  module, because I want something portable.  To ensure a low latency, I need as lightweight
  a network as is feasible for the task at hand and I certainly need to be careful about the whole image
  pipeline at runtime: both the camera feed specifications and image preprocessing.


#### Consequences

The fallout of these constraints is not only that I'm engaged in a tightrope act, but also that
I need to be careful in how I devise a metric by which I judge the outcome.  Even restricting to
a small subset of signs, assuming an appropriately chosen network architecture, training
mechanism, hyperparameters and so on, I probably don't have enough time to train such a model to its
(internally-speaking) optimal state. 

Clearly, I can't specify the details of this metric at the outset, because it depends quite
explicity on project progression; it is about putting hard numbers to the fluffy parts of the
constraints above.  However, I should be able to state it clearly a posteriori.

Moreover, it also affects what I mean by "alerting the driver".  It's evident that I would need
quite a bit more contextual information to notify the driver in an "intelligent" way: are they
breaking the speed limit; which of the potentially many signs in the frame refer to them; etc.  Such
questions must be postponed to another day.

Anyway, let's get on with getting on ...
