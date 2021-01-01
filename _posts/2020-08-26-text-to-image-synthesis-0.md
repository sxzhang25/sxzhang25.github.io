---
layout: post
title: "text-to-image synthesis, part 0: a shallow dive into GANs"
date: 2020-08-26
tags: papers text-to-image gans autoencoders
refs:
  - >
    Goodfellow, Ian, et al. "Generative adversarial nets." <i>Advances in Neural Information Processing Systems.</i> 2014.
  - >
    Salakhutdinov, Ruslan, and Geoffrey Hinton. "Deep boltzmann machines." <i>Artificial Intelligence and Statistics.</i> 2009.
  - >
    Rocca, Joseph. "Understanding Generative Adversarial Networks (GANs)." <i>towards data science.</i> 7 Jan 2019. <a href="https://towardsdatascience.com/understanding-generative-adversarial-networks-gans-cd6e4651a29">https://towardsdatascience.com/understanding-generative-adversarial-networks-gans-cd6e4651a29.</a> Medium.com. Accessed Aug 2020.
  - >
    Altosaar, Jaan. "Tutorial - What is a variational autoencoder?"<i>jaan.io.</i> 18 Jul 2016. <a href="https://jaan.io/what-is-variational-autoencoder-vae-tutorial/">https://jaan.io/what-is-variational-autoencoder-vae-tutorial/.</a> Accessed Aug 2020.
  - >
    Volodymyr Kuleshov and Stefano Ermon. "Variational auto-encoders." <i>Stanford CS228 Notes.</i> <a href="https://ermongroup.github.io/cs228-notes/">https://ermongroup.github.io/cs228-notes/.</a> Accessed Aug 2020.
---

I've been playing a lot of online games this summer. Since the pandemic hit, my friends and I have been scheduling weekly game nights in an effort to see each other and keep in contact, especially as prospects of experiencing our last year of college on-campus dwindle. Some group favorites have included <a href="https://codenamesgame.com/">Codenames</a>, <a href="https://www.geoguessr.com/">GeoGuessr</a> and <a href="https://skribbl.io/">skribbl.io</a>. The last game is a pictionary-style game where players take turn drawing words in a limited amount of time, and other players must try and guess the word as quickly as possible. After a month of playing this game, I started wondering--what would it take for a computer to act as the artist in this game?

<!--excerpt-->

<h3>the problem statement</h3>

In computer vision, the aforementioned task can be reduced to the problem of <i>text-to-image synthesis.</i> As the name suggests, the goal of text-to-image synthesis is for the model to generate a plausible image for a given text caption. Text input, image output. This challenge consists of two sub-challenges. First, the output image must look plausible--that is, there should be some visual coherence to the image. Second, the image must match the input text. For example, if the input is "A woman paddling on a surfboard at sunset," then we should expect to see the ocean, a figure in the water assuming some sort of paddling position, and some brilliant orange and purple hues in the sky. More often than not, the resulting images look pretty good from far away, but upon closer inspection it will appear that we are looking at more of an impressionist painting than a realistic image: colors and textures form blobular objects that resemble the objects in the text, but not quite perfectly. 

<h3>generative networks</h3>
This task is a textbook example of something that a generative adversarial network, or GAN, might be able to handle. Loosely, a GAN is like a game between an art forger and an art dealer. Given a description of a scene, the forger attempts to create an image that tricks the dealer into thinking that the image matches with the description. The dealer himself is trying to differentiate between images that truly match the text description and images that don't make any sense alongside the text description. Ideally, after many rounds of training, the forger has achieved a level of artifice that can successfully deceive the dealer, and ultimately, the human eye.

In proper terminology, the art forger is called the <i>generator</i> and the art dealer is called the <i>discriminator</i>. This game is formulated as a minimax optimization problem, with the generator and discriminator attempting to minimize and maximize the same loss, respectively. More precisely, for a generator $$G$$ and a discriminator $$D$$, this loss is defined as

$$
\mathcal{L}(D,G) = \mathbb{E}_{\mathbf{x}\sim p_{data}(\mathbf{x})}[\log D(\mathbf{x})] + \mathbb{E}_{\mathbf{z}\sim p_\mathbf{z}(\mathbf{z})}[1 - \log D(G(\mathbf{z}))],
$$

where $$p_{data}$$ is the probability distribution of the data, and $$p_\mathbf{z}(\mathbf{z})$$ is the prior probability distribution on a Gaussian noise random variable.<a href="#footnote1"><sup>1</sup></a> Here, $$G(\mathbf{z})$$ represents the image generated by $$G$$ given a prior noise variable $\mathbf{z}$, and $$D(\mathbf{x})$$ outputs the probability that $$\mathbf{x}$$ is sampled from the actual data. We denote the learned distribution of $$G$$ by $$p_g$$ (recall that $$G$$ is also generating random images from its own distribution, according to its parameters in the network). Written as an objective, the loss is

$$
\min_G \max_D \mathcal{L}(D,G).
$$

This makes sense, because the discriminator wants to push the probability inside the first expected value term as close to the maximum of 1 as possible, as $$\mathbf{x}$$ is being sampled from the true data. In the second expected value term, $$D$$ wants to minimize the probability $$D(G(\mathbf{z}))$$, since $$G(\mathbf{z})$$ are fake images. This would maximize the second expected value term. On the flip side, $$G$$ is attempting to fool the discriminator as much as possible, which means $$G(\mathbf{z})$$ should push $$D(G(\mathbf{z}))$$ as close to 1 as possible, thus minimizing the loss for any given $$D$$.

In the original paper <a href="https://arxiv.org/pdf/1406.2661.pdf"><i>Generative Adversarial Nets</i></a>, authors Goodfellow et al. show that this game achieves a theoretical global optimum when $$p_g = p_{data}$$. That is, the objective achieves a global minimum when the distribution of $$G$$ matches the distribution of the data. This is exactly what we want! In this case, the generator has mimicked the distribution of the data perfectly, which means that there is no way any discriminator can distinguish between an image sampled from the data and an image sampled from $$G$$. In practice, we may not achieve this global optimum exactly, but this result tells us that our objective is aptly defined. One important note to make is that in practice, training $$G$$ to minimize $$\log(1 - D(G(\mathbf{z})))$$ doesn't work because $$G$$ starts out poor and thus $$D$$ can easily predict $$D(\mathbf{x})$$ to be close to zero. This would cause $$\log(1 - D(G(\mathbf{z}))) \approx 0$$, which would saturate (i.e. effectively kill) the gradient and prevent any learning for $$G$$. To resolve this, we instead replace minimizing $$\log(1 - D(G(\mathbf{z}))$$ with maximizing $$\log(D(G(\mathbf{z}))$$, which is also equivalent to minimizing $$-\log D(G(\mathbf{z}))$$. This provides better gradients for learning early on, and maintains the same global optimimum results as before.

There are some other mathematical details involved as well, particularly with the issue of how exactly we sample from these complicated distributions. <a href="https://towardsdatascience.com/understanding-generative-adversarial-networks-gans-cd6e4651a29">This Medium article</a> gives a really good introduction to GANs from a probability perspective, and explains the some of the concepts used in sampling and comparing distributions.

<h3>GANcestors and other relatives</h3>

Although GANs were a breakthrough in generative architectures, they were preceded by many other models. The Boltzmann machine was one of the earliest generative models, using an energy-based representation to capture and take advantage of probabilistic structures within the data. The Boltzmann machine was later modified into a <a href="http://proceedings.mlr.press/v5/salakhutdinov09a/salakhutdinov09a.pdf">Deep Boltzmann machine</a> (formed by stacking layers of Boltzmann machines on top of one another), which Salakhutdinov and Hinton show can successfully generate new samples based on the training data, in their paper of the same name. Belief networks were also another probabilistic graphical model that gave rise to a "deep" version that could be used for generating novel samples, unsurprisingly named a <a href="http://scholarpedia.org/article/Deep_belief_networks">Deep Belief Network.</a>

Aside from GANs, there is also another relevant family of learning models that combines deep learning and probabilistic inference, known as <i>variational auto-encoders.</i> There are two parts to this name. The first is "variational," which is due to the fact that these models perform variational inference to learn a latent distribution. At a very high level, variational inference aims to find the best approximation $q$ of an intractable distribution $p$ over a family of tractable distributions $Q$. The task of finding the best approximation $q \in Q$ for $p$ is posed as an optimization problem. This is useful because the posterior distributions $p(z \mid x)$ which we are interested in are often computationally intractable, and thus we aim to instead approximate it. Here, $z$ may represent some sort of representation of latent variables in our inputs. For example, if our input is a set of images of a face, $z$ might encode the pose, oral expression, eyebrow positions, etc. A computer can't observe these variables directly (it only sees the values of the pixels), which is why they are latent variables. Once we know this posterior distribution, we can then use it to sample for values of $z$. The second part of the name, "auto-encoders," comes from the fact that the model is trained to learn an encoding of the input, which can be effectively decoded back into a reconstruction of the original input. This decoding part is what the model uses to generate new samples. There's a lot of probailistic results and concepts that motivate the definition of variational auto-encoders, and there are many great mathematical notes online about this, such as <a href="https://jaan.io/what-is-variational-autoencoder-vae-tutorial/">here</a> and <a href="https://ermongroup.github.io/cs228-notes/extras/vae/">here.</a>

<h3>GANs for text-to-image synthesis</h3>
The task of text-to-image synthesis requires that we create an image <i>not</i> directly from a large dataset, but rather from an arbitrary sentence or caption. Thus, there is a little more modification needed to connect the text input to the GAN portion. In particular, we need to concretely define how exactly the network should encode information about the words from the text and the relationships between them; how the GAN should interpret and use these text encodings; and how to handle auxiliary components of the image that may not be encoded in the text.

The exercise of breaking down my own thought process while playing skribbl.io was a neat way of thinking about this task, because it ascribes to the text-to-image synthesis pipeline a natural performance metric: given an image, how well can a player recover the original text input? In this case, the inputs are just nouns, so the recovery part is much less complicated in some respects. But skribbl.io has a lot of built-in restrictions that force us to perform a lot of cognitive tasks that we don't even think about. For example, there are many ways to draw images so that the other players can guess the correct word, just as there are many possible images corresponding to a piece of text (known as <i>multimodal learning</i>). Also, we may only have 30 seconds to produce a drawing of a complex noun like "nature."<a href="#footnote2"><sup>2</sup></a> Clearly, we will have to draw multiple objects to describe nature, since it is an abstract noun. But what objects do we choose? How can we ensure that the scene we create does not lead people to guess "forest" or "habitat" or "park" instead? Do we even need to draw a scene, or is it enough to draw disparate flora and fauna? And if the other players are moving in an incorrect direction, how do we use their wrong guesses to refine our image? 

I like coming up with these questions because although they seem obvious, wording them precisely and specifically can be tricky. Obviously, some of these questions begin to stray away from the text-to-image synthesis task. A key difference between the two scenarios is that the image generated by the model does not have to strongly imply a singular word, but generally match the spirit of the text. So the text-to-image portion of the computer vision task is much more important, whereas both text-to-image and image-to-text directions might be considered equally important in skribble.io. Also, the plausibility requirements are much stricter in the computer vision task--you can be a terrible artist but still succeed in skribbl.io. But the essence of representing some text as an image in a way so that the text can be recovered is there. And we can model the other players as networks too, trained to understand and describe scenes (so, image-to-text). Perhaps these two components can work together in their own collaborative learning setting as well. There are so many ways to look at it!

<div class="footnotes">
<hr align="left" size="1">
<section id="footnote1"><sup>1</sup>The $\sim$ means "sampled from." So the expected values are taken with respect to $\mathbf{x}$ sampled from the data, or $\mathbf{z}$ sampled from $p_\mathbf{z}$, which is a Guassian noise distribution. To produce this symbol in LaTeX, use the command $\text{\sim}$.</section>

<section id="footnote2"><sup>2</sup>True story. I did not guess this word in time.</section>
</div>