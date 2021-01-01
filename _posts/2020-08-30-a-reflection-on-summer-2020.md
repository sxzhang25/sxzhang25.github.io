---
layout: post
title: "a reflection on summer 2020"
date: 2020-08-30
tags: programming internship
refs:
---

This has been a crazy summer.

Well, not in the traditional sense. My day-to-day life has actually been relatively quiet from the perspective of an outsider (which I know is an incredible privilege). But life around the world has effectively erupted into chaos, and in a single year the US has seen a societal shift in how we view our politics, our priorities, and our social interactions. Living through the last six months has taught me some invaluable lessons, and forced me to think hard about my values and goals. Despite everything that has happened this summer, I am still in a position to be grateful for many things, and I wanted to take some time and record those gratitudes.

<!--excerpt-->

<h3>what I learned from google</h3>

This summer was my first "real" internship and experience working in a big company (seriously, big). I was extremely lucky to have been placed on a team that I had been excited about long before I applied to intern there, and only grew to love as the internship progressed. Due to COVID-19, Google opted to switch its internship to a virtual model--meaning I would not be working at Google's Mountain View headquarters, but from my own room at home. Although this was definitely not ideal, I still managed to have a good time.

I was an intern on the Pixel camera intelligence team, working with a subgroup that focused on using computer vision and machine learning to improve the camera experience. Although I'm admittedly an iOS user, the one thing that has kept the Pixel in my mind is its camera. As an artist, I have always responded best to visuals, and the Pixel's intense focus on solid computational photography seemed like the perfect place for creative engineering. The intelligence team is just one of the subteams that engineers all the Pixel's incredible camera software features, from <a href="https://ai.googleblog.com/2019/11/astrophotography-with-night-sight-on.html">Night Sight</a> to <a href="https://ai.googleblog.com/2018/12/top-shot-on-pixel-3.html">Top Shot</a> to <a href="https://ai.googleblog.com/search/label/Computational%20Photography">HDR+</a>.<a href="#footnote1"><sup>1</sup></a> I was beyond ecstatic to have the opportunity to work with them, and I still find myself in disbelief even after it has ended.

I went into the summer with a lot of enthusiasm. But honestly, that was kind of it! I had never worked a software engineering role before, and the programming concepts that are needed to build real things in the real world are <i>completely</i> different from what you learn in computer sciences classes at a liberal arts school. In school, classes tend to focus on theory (which I acknowledge is very important), but algorithms alone can't build complex systems with complex interactions. At Google, I had the chance to learn and leverage Java and programming concepts that I had only heard of before--Futures, Handlers, Executors, concurrency; I got to dip my toes into the incredibly vast and deep world of graphics programming; I got to develop and test on an actual Pixel phone that they shipped to me! Though I only scraped the surface with all of these ideas, I feel like I've already surmounted the steepest part of the learning curve. And all of this was only made possible by my incredibly patient and helpful managers.

<h3>thoughts from a novice software engineer</h3>

I would categorize a lot of what I learned this summer under technical programming concepts. That is, I picked up a lot of new programming tools that helped make me a better developer. However, I also discovered that there is a vast amount of knowledge concerning <i>how</i> to work effectively as an engineer that I still need to improve on. The use of engineering paradigms is probably the most important one. Paradigms are sort of like different schools of thought within coding, and they dictate how programmers architect and write their code. They can be just about anything--for example, the <a href="https://gist.github.com/staltz/868e7e9bc2a7b8c1f754">reactive programming paradigm</a> (or "Rx" paradigm) is a broad programming paradigm that emphasizes propagations of change (hence, reactive), whereas the <a href="https://martinfowler.com/bliki/FluentInterface.html">fluent interface paradigm</a> focuses on writing and organizing code in a human-readable way. Properly using these paradigms can make code more robust and more accessible.

After working alongside pretty senior engineers this summer, I definitely realized just how distanced real software engineering is from the type of work found in undergraduate computer science programs. In industry, the importance of solving problems lies not necessarily in the cleverness or elegance of the algorithm (and indeed, many times the algorithm has already been written and is thus abstracted away from concern anyway), but rather in the industrial strength of the solution. The idea that code is a "language" rather than a tool becomes much more apparent, and communicating effectively with this language is an art. In academia, programming is more of a tool for performing experiments, although code clarity and cleanliness is still important for efficiency and reproducibility. But even within industry there seems to be a broad horizontal spectrum of how research-facing or product-facing an engineering role is. For example, a front-end engineer might be working on improving a user's mobile experience, whereas a research engineer may be optimizing a learning algorithm that isn't even being used in a product. I'd say that the work on the camera intelligence team leans more towards the latter, but they still get to maintain some proximity to the user because the camera app is such a core application.

There's also another spectrum in the tech industry, which is the vertical, heirarchical spectrum within a company. Especially at large companies, as you move up this spectrum it generally entails more strategizing and managing, and less building and coding. An interesting piece of advice I once got from an engineer (not at Google) was that if you enjoy the level of intimacy with a project that coding provides, then sacrificing that proximity to programming may not always be worth moving up another step in the management ladder. This piece of advice has stuck with me for a long time because it was the first time I heard an engineer frame their career progress in terms that didn't include getting promoted. That being said, I also learned from many engineers this summer that becoming a manager is a form of huge personal growth in its own right, and not necessarily just about making more money. At Google, I felt like this vertical spectrum was still pretty subtle--the manager of my team always gave extremely specific technical suggestions to problems that interns ran into, and I really appreciated that. 

<h3>work outside of work</h3>

During evenings and weekends after work, I continued to explore my junior year independent work project from the spring semester. I wouldn't call it full on "research," but I did have to look through a lot of papers, generate data and run a lot of experiments throughout the summer. Every now and then, I would sync up with my project advisor to discuss my progress and possible next steps. This has been the most long-term project I've worked on to-date, and it's one of the primary experiences that has influenced my attitude towards graduate school. Despite not having the deepest background in the project area, I'm really enjoying the combination of code, data analysis and applied math that goes into the research. The timeline of the project also gave me a (very preliminary) stress test of how I might handle the highs and lows of a four or five year PhD program.

Like my managers at Google, my project advisor has played an incredibly instrumental role in my ability to grow as a researcher. I've heard countless times that choosing the right advisor is one of the most important parts of a PhD, and working alongside my advisor has convinced me that this is true. Being an undergraduate, I've relied on his guidance and mentorship much more than I'd imagine a PhD student would rely on hers, and I'm extremely grateful that he was willing to dedicate this energy to helping me. One extremely important lesson I've learned is that academic researchers always know how to ask the right questions. By "right," I mean critical in a productive way--these questions might catch you off guard or stump you, but thinking about them and (hopefully) answering them is sure to make the rest of your work more robust. Getting caught with a question like this is most certainly not the best experience, but it's a necessary and valuable one.

I'm also glad that I chose to stick with a project within the math department. While my project is in applied mathematics and data science (and not pure math), operating within the realm of mathematics means that theory motivates all the decisions. So, even though I may be running experiments and designing algorithms, all the choices I make need to be motivated (and ideally justified) by proven results. In the context of data science, these relationships are usually statistical properties and asymptotics. This is something that I really had to get used to. For instance, there was a point in my research when I was getting some really solid results after I made a few "improvements" to one part of the algorithm I was running. These improvements, however, were purely algorithmic--they sought to optimize results based on the data, not based on any mathematical reasoning. When I showed my advisor the results, he immediately asked me why I had made those changes, and what mathematical significance they had--and of course, I couldn't give him a good answer other than, "it worked on this one dataset."

Even as I transition into computer science, I want to maintain this philosophy. In the space of deep learning and neural networks especially, I think that there is an increasing reliance on accuracies and empirical evidence to promote new model architectures. While I believe running experiments is an important part of researching these immense and complex systems, I wonder if this results-driven approach to deep learning is exacerbating the obfuscation of the inner workings of deep neural networks.<a href="footnote2"><sup>2</sup></a> I don't have a complete view of research in this area yet and so this opinion may be prematurely formed, but I hope I can continue to keep in close touch with the math at the center of AI systems.

<h3>looking ahead</h3>

I was definitely gutted back in May when I learned I would not be experiencing life in California as originally planned, but instead staying at home for the summer. But looking back, it wasn't a bad summer at all. The upcoming semester is going to be uncharted territory once again, and although the situation is not ideal, I feel like I'm happy with where I am.

<div class="footnotes">
<hr align="left" size="1">
<section id="footnote1"><sup>1</sup>A lot of engineers on my team were actively involved in the project mentioned in these blogs, and some of them even co-authored or got shout-outs in them!</section>

<section id="footnote2"><sup>2</sup>Understanding the inner workings of deep neural networks seems like such an incredibly cool field of research. And especially since these tools are being deployed at such massive scales now, I think that understanding how these models work is extremely important.</section>
</div>