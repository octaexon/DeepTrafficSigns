### Links
[home](../README.md) &#8226; [intro](introduction.md) &#8226; [env](environment.md) &#8226;
[data](data.md)

### Data

Before we can decide what to do, we need to get some understanding of what we have at our
disposal.  

#### Bounding the extent of the challenge

Focussing on the recognition stage for a moment, a comprehensive road sign classifier is
a significant undertaking. The number of distinct signs on our roads is incredibly large and ever
increasing. For example, here's a sign we didn't have on our roads until recently:

<img class="display" src="elektrisch.png">

Evidently, I need to place restrictions to ensure feasibility.

- **descriptive**  The majority of signs are descriptive (e.g. direction, location etc.):

    <img class="display" src="hannover.png" width="200rem">

  Textual comprehension is beyond the scope of this project; I will restrict to
  symbolic comprehension. 

- **Vienna convention** Road signs are standardized by the [Vienna Convention on Road Signs and
  Signals](https://en.wikipedia.org/wiki/Vienna_Convention_on_Road_Signs_and_Signals).  This is a
  multilateral treaty designed to increase road safety and which the majority of European
  countries have ratified.  It categorizes signs into one of 8 groups:  

  |warning                                              |priority                                           |prohibitory                                           |mandatory                                               |
  |:---------------------------------------------------:|:-------------------------------------------------:|:----------------------------------------------------:|:------------------------------------------------------:|
  |<img class="display" src="danger.png" width="100rem">|<img class="display" src="stop.png" width="100rem">|<img class="display" src="noentry.png" width="100rem">|<img class="display" src="mandatory.png" width="100rem">|


  |special                                                |informative                                             |indicative                                             |additional                                        |
  |:-----------------------------------------------------:|:------------------------------------------------------:|:-----------------------------------------------------:|:------------------------------------------------:|
  |<img class="display" src="children.png" width="100rem">|<img class="display" src="waterprot.png" width="100rem">|<img class="display" src="autobahn.png" width="100rem">|                                         <img class="display" src="wet.png" width="100rem">|


  
  
  

  and prescribes certain characteristics: shapes, colors, sizes.  Having said that, in any given
  country, there are certainly large numbers (>500) of distinct symbolic signs (see
  [here](https://en.wikipedia.org/wiki/Road_signs_in_Germany) for a sample of German signs and
  [here](https://www.dvr.de/publikationen/downloads/verkehrszeichen.html) where I located some nice
  pngs). Again, with an eye to future data collection, I will restrict to a very small number.


- **intraclass variety** For any given sign, there are very often national differences in the
  precise realization of signs, even among those countries signed up to the Vienna convention. For
  example, a quick look at
  [Wikipedia](https://en.wikipedia.org/wiki/Comparison_of_European_road_signs) yields the following:

  <img src="train_austria.png" width="120rem">
  <img src="train_belgium.png" width="120rem">
  <img src="train_czech.png" width="120rem">
  <img src="train_denmark.png" width="120rem">
  <img src="train_estonia.png" width="120rem">
  <img src="train_finland.png" width="120rem">
  <img src="train_france.png" width="120rem">
  <img src="train_germany.png" width="120rem">
  <img src="train_greece.png" width="120rem">
  <img src="train_hungary.png" width="120rem">
  <img src="train_netherlands.png" width="120rem">
  <img src="train_norway.png" width="120rem">
  <img src="train_poland.png" width="120rem">
  <img src="train_portugal.png" width="120rem">
  <img src="train_romania.png" width="120rem">
  <img src="train_russia.png" width="120rem">
  <img src="train_slovakia.png" width="120rem">
  <img src="train_slovenia.png" width="120rem">
  <img src="train_spain.png" width="120rem">
  <img src="train_sweden.png" width="120rem">
  <img src="train_switzerland.png" width="120rem">
  <img src="train_turkey.png" width="120rem">
  <img src="train_ukraine.png" width="120rem">
  <img src="train_uk.png" width="120rem">

  However, my data sources are unlikely to be so diverse. I'm based in Berlin, so any manual data
  collection will be local and as I'll discuss below, my core dataset is sourced in Germany, so
  I should expect a classifier that deteriorates in performance outside of Germany.  This is really
  not a concern for my project, as my live testing will also occur here.



#### GTSDB

As I stated earlier, the core dataset comes from the GTSDB (German Traffic Sign Detection
Benchmark). This [link](http://benchmark.ini.rub.de/Dataset_GTSDB/FullIJCNN2013.zip) downloads the
associated zip file and on the surface, it's a relatively meaty 1.6GB.  Unfortunately, the files are
in the rather inefficient Portable Pixmap format (24-bit-color images where each pixel is encoded as
uncompressed text). On closer inspection, there are only 900 images spread across 43 classes. Here
is their distribution:

<svg class="chart"></svg>

As its name suggests, this is a benchmarking dataset, so one course of action, would be to compare
any model I construct against the benchmark.  However, I'm not motivated to go down that road and
you can see why if you look inside the dataset: even within the more frequently occurring classes,
the environment is not particularly diverse. Of course, road signs occur *at roads*, so one
shouldn't expect a magical wonderland of diversity, but:

- **weather** Typically German, mostly cloudy with some sunny scenes. However, adverse
  conditions: rainy, sleety, stormy, snowy are underrepresented (some do not occur at all).

- **illumination** All are taken during the day, sunrise and sunset are underrepresented and
  nighttime scenes are completely absent.

- **line of sight** While there are examples of signs falling in varying degrees of shadow and some
  with moderate blur, no occlusion occurs.

Certainly, some of the signs are difficult to read so models doing better on this benchmark are
probably better in real life, but the benchmarking error rates are unlikely to hold any
precise meaning for real world applications. 

Given the constraints detailed [earlier](introduction.md), I find it more interesting (and indeed
more feasible) to develop a model restricted to a very small number of signs and attempt to evaluate
on live test data in a variety of conditions.


#### Statement of intent

I picked the following signs:

|priority road                                 |give way                                   |speed limit 30                          |speed limit 50                          |
|:--------------------------------------------:|:-----------------------------------------:|:--------------------------------------:|:--------------------------------------:|
|<img src="chosen_priority.png" width="120rem">|<img src="chosen_yield.png" width="120rem">|<img src="chosen_30.png" width="120rem">|<img src="chosen_50.png" width="120rem">|

for the several reasons:

- **frequency** They are among the most frequent in the GTSDB dataset. Moreover, I live within city
  limits, and generally 50km/h is the default speed limit within a German city, with 30km/h for
  smaller streets.  Since it is a small dataset a major consideration is the ability to collect more
  data.

- **interclass variation** It tests two criteria: that the model can pick out various shapes and
  colors (admittedly, this should be easily satisfied within the relatively high capacity models
  that I'm going to consider) and that it can pick out subtler differences (the speed limit signs
  differ only in the text).

With preliminary data at hand, let's pick out the models.

<style>

img.display {
    display: block;
    margin-left: auto;
    margin-right: auto;
}

.chart rect {
  fill: steelblue;
}

.chart text {
  fill: white;
  font: 10px sans-serif;
  text-anchor: end;
}

</style>
<script src="//d3js.org/d3.v3.min.js" charset="utf-8"></script>
<script>

var width = 600,
    barHeight = 15;

var x = d3.scale.linear()
    .range([0, width]);

var y = d3.scale.ordinal();

var chart = d3.select(".chart")
    .attr("width", width);

d3.json("class_frequencies.json", function(error, data) {
  x.domain([0, d3.max(data, function(d) { return d.frequency; })]);

  chart.attr("height", barHeight * data.length);

  var bar = chart.selectAll("g")
      .data(data)
      .enter()
      .append("g")
      .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

  bar.append("rect")
      .attr("width", function(d) { return x(d.frequency); })
      .attr("height", barHeight - 1);

  bar.append("text")
      .attr("x", function(d) { return x(d.frequency) - 3; })
      .attr("y", barHeight / 2)
      .attr("dy", ".35em")
      .text(function(d) { return d.frequency; });
});

</script>
