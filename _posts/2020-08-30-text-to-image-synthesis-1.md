---
layout: post
title: "text-to-image synthesis, part 1: learning to draw"
date: 2020-08-30
tags: papers text-to-image computer-vision machine-learning
refs:
  - >
    Gregor, K., Danihelka, I., Graves, A., Rezende, D., and Wierstra, D. "Draw: A recurrent neural network for image generation." In <i>ICML</i>, 2015.
---

As I mentioned in <a href="https://sxzhang25.github.io/blog/2020/08/26/text-to-image-synthesis-0">my previous post</a> introducing the text-to-image (T2I) synthesis task, there are two main parts to this task: (1) producing a suitable encoding of the text input and (2) creating a plausible image from the text encoding. You might also add in a third part, which is defining exactly how the information in the text encoding should be used in the image generation, but I feel like this is a more open-ended challenge that deserves its own discussion. In this post, I want to focus independently on an interpretation of the second task.

<!--excerpt-->

<h3>drawing pictures vs. generating images</h3>

Before I became interested in the T2I task, I had originally set out to find papers that might help me understand what it would take to train a model to produce drawings of a word or phrase (like you would do in a game of Pictionary). So as I was looking through the references in few different T2I papers, I noticed that many of them cited this paper called <a href="https://arxiv.org/pdf/1502.04623.pdf">DRAW: A Recurrent Neural Network for Image Generation</a> by researchers at Google DeepMind. The first few sentences of the paper read,

<blockquote>
"A person asked to draw, paint or otherwise recreate a visual scene will naturally do so in a sequential, iterative fashion, reassessing their handiwork after each modification. Rough outlines are gradually replaced by precise forms, lines are sharpened, darkened or erased, shapes are altered, and the final picture emerges. Most approaches to automatic image generation, however, aim to generate entire scenes at once."
</blockquote>

From what I've read on GANs and image generation, it seems very true that oftentimes the task of image generation is approached from a top-down perspective. In contrast, most people create pictures in a highly structured manner, organizing scenes by objects, objects by parts, and parts by anatomy. The process described by the researchers above is true as well, especially in classical painting: artists begin with a sketch or underpainting that roughly outlines the scenes, then they go in and render rough values, and after that comes subsequent iterations of refinement and detailing. Within each of these broad steps, the artist will move along in the aforementioned organized fashion.

<div class="footnotes">
<hr align="left" size="1">
<section id="footnote1"><sup>1</sup>The $\sim$ means "sampled from." So the expected values are taken with respect to $\mathbf{x}$ sampled from the data, or $\mathbf{z}$ sampled from $p_\mathbf{z}$, which is a Guassian noise distribution. To produce this symbol in LaTeX, use the command $\text{\sim}$.</section>

<section id="footnote2"><sup>2</sup>True story. I did not guess this word in time.</section>
</div>