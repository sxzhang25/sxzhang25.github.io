---
layout: post
title: "a brief account of cvpr 2020"
date: 2020-06-22
refs:
  - >
    Carion, Nicolas, et al. "End-to-End Object Detection with Transformers." <i>arXiv preprint arXiv:2005.12872</i> (2020).
  - >
    Menon, Sachit, et al. "PULSE: Self-Supervised Photo Upsampling via Latent Space Exploration of Generative Models." <i>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition.</i> 2020.
  - >
    Miolane, Nina, and Susan Holmes. "Learning Weighted Submanifolds with Variational Autoencoders and Riemannian Variational Autoencoders." <i>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition.</i> 2020.
---

Yesterday marks the end of another Computer Vision and Pattern Recognition (CVPR) conference. CVPR had first come onto my radar back in December 2019 when I had discovered that my internship would be located in Mountain View, CA, a mere two-hour flight from the conference's hosting city of Seattle, WA. Unsurprisingly, the conferenced ended up taking on a virtual form, meaning all the talks, Q&A's, and live sessions would have to be conducted via online video chats. I still ended up signing up, but since I would be working at the same time and the conference wouldn't be such a physical, immersive experience, I only checked in occasionally. That being said, I did get to access a huge collection of amazing computer vision research, and I definitely want to attend an in-person iteration of the conference in the future.

<!--excerpt-->

<h3>a virtual conference</h3>

I've been to one other academic conference in the past, which was MathFest 2019.<a href="#footnote1"><sup>1</sup></a> That was my first academic conference experience ever, and I actually gave a talk there with my research peers at the time. In a typical conference, attendees typically have their own presentation slot, and spend the rest of the week going to keynotes, smaller presentations, and poster sessions. These different formats provide the attendees and presenters with a variety of levels of engagement, but they all share the same veritable degree of immersion and participation in a physical event.

The virtual setup of CVPR relied mostly on Zoom, providing links to attendees to enter a live video chat with presenters and speakers at a given time.<a href="#footnote2"><sup>2</sup></a> Presentations were also made available online in video form, so that attendees could watch them at any time without a live or interactive component. Since CVPR attendees typically come from time zones all around the world, it was important that these presentations could be available at all times. Live sessions were thus given in two rounds: once at their regularly scheduled time slot in PDT, and another time 12 hours later to accommadate attendees in Asia and continents. Interactive raffles with sponsors were replaced with tallies of virtual interactions with sponsor webpages, and casual banter was supported via live chat widgets. I will say that based on the dearth of comments in those chat windows (and also the complaints in the messages that were shown), chat windows will simply never replace the forum for small talk and networking that a physical conference provides. Of course, given that the conference providers had planned for a physical event and had such little time to switch this entire event over to a virtual setting, I think that they did a great job.

<h3>some interesting tidbits, part 1</h3>

I did not get to attend the conference with as much attention and concentration as I would have liked, but I did get to pop into a few sessions and learn some really cool things. The first event I attended was a Deep Learning and Geometric Computing workshop. The presenters went over some traditional and current methods in 3D reconstruction and graphics, including camera-based reconstruction, which is a big area of research is developing autonomous vehicles; the geometrical pitfalls and blessings of working with high-dimensional data; and reconstructing 3D representations of people and objects with which people commonly interact.

I particularly enjoyed Professor Mireille (Mimi) Boutin's keynote on high-dimensional data because it highlighted and revisited a lot of topics my junior seminar in the Fall 2019 semester talked about. She translated her talk really well into a livestream format by drawing diagrams and figures live, as if she was teaching a virtual class. She gave this extremely luculent explanation on the problem of density in high dimensions, which I've attempted to recreate in Figure 1. Essentially, data sampled from a nondegenerate distribution function on a cube tend to lie at the boundary of the cube, and as the number of dimensions tends towards infinity the probability of sampling a data point from the interior of the cube shrinks to zero. Machine learning methods that rely on metric-based discrimination may also suffer performance losses because discrepancies in distances tend to decrease, regardless of metric. This is a very relevant issue in computer vision, because computer vision datasets often live in high-dimensional spaces and hence these datasets risk the danger of becoming too sparse to reliably analyze.

<figure>
  <img src="https://github.com/sxzhang25/sxzhang25.github.io/raw/master/imgs/2020-06-22-fig1.png" alt="The curse of dimensionality for hypercubes" style="width:100%">
  <figcaption>Figure 1. A re-illustration of how Professor Boutin explains one of the curses of dimensionality. In math classes, there can be this overwhelming tendency for formalities that completely abstract away any visual intuition of the subject matter, so I really appreciated her use of figures.</figcaption>
</figure>

The natural solution to dimensionality is to represent high-dimensional data using lower dimensional spaces, via methods such as principal copmonent analysis (PCA) or diffusion maps. An immediate problem here is that projections can destroy the rich structures present in higher dimensions, since using lower dimensions means adopting a courser representation. However, what Prof. Boutin also points out is that projections can <i>create</i> structure as well. For extremely high-dimensional data, these structures can be spurious and misleading. This is because clusters are relatively easy to find in such high dimensions; moreover, there are potentially many ways to cluster the data. Thus projection methods might unintentionally highlight a particular way of clustering the original data at the expense of masking other ways. Which ways of clustering are better? Usually, there's no obvious answer. In fact, Prof. Boutin suggests that the entire clustering problem may be ill-posed until this question is addressed.

The rest of the keynote was structured around measuring the clusterability of different random projections. This talk really made me wish I had spent some more time in the past three years taking statistics classes, but if I'm being entirely honest the offerings of good mathematically-focused statistics courses at Princeton are rather bare. Using the clustering of digits based on the vertices of a $$d$$-dimensional cube, Prof. Boutin demonstrated the range of expression that such clustering methods capture. The different vertices actually end up describing very semantically interpretable features of numerical digits, such as the similarities between 7's, 9's and 2's, or the slantedness of some people's 1's versus the straightness of other people's 1's, or even the distinctive circular shape of 0's. It was a really neat experiment to see.

<h3>some interesting tidbits, part 2</h3>

I also took some time to attend the tutorial on Visual Recognition for Images, Video, and 3D hosted by Facebook AI Research (FAIR). This included a survey on current object detection problems and methods, starting with image segmentation and moving up through 3D mesh segmentation. I was really excited about this tutorial because I had seen <a href="https://twitter.com/jcjohnss/status/1242882312641155072">a tweet</a> displaying one of the applications of the 3D mesh detection methods.

Before this workshop, I had seen a lot of material on object segmentation from my two computer vision classes, but this tutorial gave me a new perpective on how the problem of segmentation is posed. Specifically, segmentation can be split into two problem philosophies: <i>instance segmentation</i>, which seeks to make pixel-level classifications of object <i>instances</i> (e.g., you can have multiple instances of a dog in an image, but you can't really have an instance of the sky--there's only one sky in the image, even if it is comprised of disjoint regions); and <i>semantic segmentation</i>, which seeks to make pixel-level classifications related to the image context. For FAIR, the future of segmentation lies in <i>panoptic</i> segmentation, which aims to perform both instance and semantic segmentation. This can be achieved via non-unified approaches, which do semantic and instance segmentation separately and later combine them, or we may opt for a bottom-up approach, which seeks to build larger classification regions by repeatedly combining local classification regions. Recent FAIR researchers have also created a unified segmentation appropach, which use a CNN and transcoders to simultaneously perform instance and semantic segmentation. This method is described in the paper <a href="https://ai.facebook.com/blog/end-to-end-object-detection-with-transformers/"><i>End-to-end object detection with Transformers</i></a> by Nicolas Carion and Francisco Massa, et al.<a href="#footnote3"><sup>3</sup></a>

The part I found most interesting was actually the qualitative metric they defined to evaluate a particular network's performance on the panoptic segmentation task. This is always a tricky part of creating new deep learning methods, because it is essential to training and interpretability--without a metric, we don't have a good starting point for defining a loss function or doing any error analysis. The difficulty of evaluating object segmentation is that misclassifications of individual pixels do not really change a segmentation result, but many different misclassifications can gradually degrade the segmentation. The researchers used a metric called Panoptic Quality (PQ) to categorize a segmentation as correct or incorrect. The idea is basically Intersection-over-Union (IoU) for segmentation.

<h3>some interesting tidbits, part 3</h3>

The last tutorial I went to was the Fairness and Accountability session hosted by Timnit Gebru and Emily Denton, two research scientists at Google. The biggest takeaway I got from this session was the inadequacy of dataset re-balancing as a cure for algorithmic bias. Many researchers believe that simply collecting more balanced datasets will solve the issue of bias in machine learning, but this is not true. In order to more accurately curate representative and inclusive data, we must collect data with diligence and care, with a focus on "privacy, transparency, and value." Without such deliberation in dataset curation, our data simply replicates existing social biases. Out of the ways to do this, the idea of creating community archives stuck with me the most, in which communities collect their own data archives to store their history and culture. I think this approach allows marginalized communities to not only represent themselves the way they believe is most authentic, but also maintain an active outlet for historical record keeping, according to their own terms.

<figure>
  <img src="https://github.com/sxzhang25/sxzhang25.github.io/raw/master/imgs/2020-06-22-fig2.png" alt="Incorrectly upsampled faces" style="width:50%">
  <figcaption>Figure 2. (a) A downsampled picture of Barack Obama (which is amazingly recognizable) that somehow turned White; (b) Images of AOC and Machine Learning Research Scientist Robert Osazuwa Ness downsampled and then upsampled using the algorithm (granted permission to use).</figcaption>
</figure>

The idea of ethics in AI is a daunting subject. More than a few times in the past week, I've become overwhelmingly stressed by going down an ethics rabbithole while thinking about AI technologies. Especially when dealing with people, there are myriad intended and unintended consequences that need to be reasoned through before proceeding. Gebru points out in her presentation that a mission statement disclosing the <i>why</i> behind a research project is particularly important. A paper from this CVPR conference actually <a href="https://twitter.com/osazuwa/status/1274444300894572546">went slightly viral</a> in the AI community for lacking these exact considerations. The paper, titled <a href="http://pulse.cs.duke.edu/"><i>PULSE: Self-Supervised Photo Upsampling via Latent Space Exploration of Generative Models</i></a> by Sachit Menon and Alex Damien, et al., describes a model that upsamples an image of a person to recover a high-resolution face; however, when famous politicians of color such as Barack Obama and AOC were put into the algorithm, they somehow became White. Ordinary faces of color underwent this surely unintentional (but still problematic) transformation as well. While the technology behind this is pretty extraordinary, I think even framing the mission of this project in a racial context would have anticipated this problem.

<h3>takeaways</h3>

I actually feel very lucky to have such large amounts of resources available for me to consume in digital form--it has allowed me to attend the conference at a much more leisurly pace than I would have taken in person. At the same time, it definitely lacked the academic excitement that an in-person conference would have inspired. I managed to speak to one poster presenter whose research was very closely aligned with my junior paper topic, and the interruptions of Zoom coupled with the lack of readily available physical materials made communication much more difficult. The paper, titled <a href="http://openaccess.thecvf.com/content_CVPR_2020/papers/Miolane_Learning_Weighted_Submanifolds_With_Variational_Autoencoders_and_Riemannian_Variational_Autoencoders_CVPR_2020_paper.pdf"><i>Learning Weighted Submanifolds with Variational Autoencoders and
Riemannian Variational Autoencoders</i></a> by Nina Miolane and Susan Holmes, actually seemed really interesting and has given me more reason to finally take a class on manifolds in the spring (my last semester!).

In terms of conference programming, I've noticed that keynotes tend to cater to a wider, more general audience; whereas presentations and poster sessions seem to be more geared towards a more knowledgeable, niche set of listeners. This makes sense, since keynote speakers usually address all conference attendees, while engaging with a particular poster is a self-selecting process. I unfortunately did not get to attend any of the live keynotes, like the fireside chat with Microsoft CEO Satya Nadella, due to schedule conflicts. In the end though, I think I probably got the most out of the conference that I possibly could, since I was working on my internship for much of the same time. I definitely want to go to another CVPR in the future (hopefully with an accepted paper!).

<div class="footnotes">
<hr align="left" size="1">
<section id="footnote1"><sup>1</sup>I just looked this up and found out that it was cancelled this summer (understandably). I feel really bad for student researchers at REUs, so many conferences and chances to practice presenting math are getting cancelled. I really hope they can hold it successfully next summer.</section>

<section id="footnote2"><sup>2</sup>According to the CVPR site, there were "7600 attendees, 25 sponsors, 5025 'event items' (papers/talks etc), and 1,497,800 minutes of zoom discussions"--pretty impressive!</section>

<section id="footnote3"><sup>3</sup>I haven't gotten a chance to read this yet, and I'm not super familiar with transcoders. I'll have to come back to this some other time.</section>
</div>