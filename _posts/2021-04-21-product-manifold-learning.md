---
layout: post
title: "learning to factorize a manifold"
date: 2021-04-20
tags: papers data-analysis statistics conferences
refs:
  - >
    Sharon Zhang, Amit Moscovich, Amit Singer. "Product Manifold Learning." In <i>AISTATS</i> 2021.
  - >
    Stefan Lafon. "Diffusion maps and geometric harmonics." PhD Dissertation, Yale University. May 2004.
---

Imagine you have some sensory data of a robotic arm moving around. Given a little bit of prior info about this mechanism, we may reasonably assume that it has several joints at which the arm moves. How can we figure out what kinds of motions each of these joints exhibits? In our recent AISTATS paper, <a href=""><i>Product Manifold Learning</i></a>, we tackle this question and others like it.

<!--excerpt-->

<h3>background</h3>

A more formal way of describing the problem above is to consider our data as observations of some signal from some latent variables $(\theta_1, \ldots, \theta_m)$ to our observable space (typically high dimension Euclidean space---think image data). If each latent variable $\theta_i$ lies on a manifold $\mathcal{M}_i$, then we can model the entire latent space as a product manifold,

$$
\mathcal{M} = \mathcal{M}_1 \times \cdots \mathcal{M}_m.
$$

However, even with this information we know nothing about the geometry of the individual $\mathcal{M}_i$'s, which we call <i>manifold factors.</i> Is there some way of recovering this from our data? For example, can we determine that the swiss roll structure in Figure 1 is actually just a rectangle that's been rolled up?

<figure>
  <img src="" alt="Unrolling a swiss roll dataset" style="width:100%">
  <figcaption>Figure 1. One way of applying dimensionality reduction to a 3D swiss roll dataset is "unroll" it as a rectangle.</figcaption>
</figure>

The answer is yes! To do so, we need some theoretical results first.

<h3>the laplacian over product spaces</h3>

The main theoretical result we can leverage is the way the Laplacian decomposes over product spaces. Consider the spectrum of the Laplacian operator, i.e. the set of solutions to the Helmholtz equation

$$
\Delta_\mathcal{M} f(\mathbf{x}) = \lambda f(\mathbf{x}), \qquad \forall \mathbf{x} \in \mathcal{M}
$$

with Neumann boundary conditions

$$
\nabla_\mathcal{M} \cdot \nu(\mathbf{x}) = 0, \qquad \forall \mathbf{x} \in \partial \mathcal{M}.
$$

We call these $f(\mathbf{x})$ the Laplacian (Neumann) eigenfunctions. When $\mathcal{M}$ is a product manifold with $m$ manifold factors, we can write every $f(\mathbf{x})$ as the product

$$
f(\mathbf{x}) = \prod_{i=1}^m \bigg(f^{(i)}_{k_i} \circ \pi^{(i)} \bigg),
$$

where $\pi^{(i)} : \mathcal{M} \rightarrow \mathcal{M}_i$ is the canonical projection. More colloquially, each eigenfunction decomposes as the product of one eigenfunction from every manifold factor. In addition, we have another nice property:

$$
\lambda_{k_1, k_2, \ldots, k_m} = \sum_{i=1}^m \lambda^{(i)}_{k_i},
$$

i.e. the eigenvalue of the eigenfunction is precisely the sum of the eigenvalues of the eigenfunctions which form the product. Lastly, these eigenvalues are all nonnegative and monotonically increasing.

To illustrate with an example, consider the simplest possible product space---a rectangle, which is the product of two closed line segments. Figure 2 shows the part of the spectrum of the rectangle, broken down into a sort of infinite multiplication table of the spectrum of each line segment.

<figure>
  <img src="" alt="Decomposition of the Laplacian over product spaces" style="width:100%">
  <figcaption>Figure 2. Each product eigenfunction of the rectangle is the product of an eigenfunction of the vertical line segment and an eigenfunction of the horizontal line segment.</figcaption>
</figure>

Borrowing some fundamental terminology, we call the eigenfunctions along the top row and left column "factor eigenfunctions" and the rest of the eigenfunctions "product eigenfunctions."

<h3>our method</h3>

Suppose we are just in the two manifold factor case right now, i.e. $\mathcal{M} = \mathcal{M}_1 \times \mathcal
{M}_2$. Minus some details, our factorization algorithm can be defined in three steps:

1. <b>Compute the spectrum of the Laplacian.</b> Since we don't have infinite data samples, we need to approximate the eigenfunctions. We can do so by computing $N$ eigenvectors of the graph Laplacian instead. For more information on the asymptotics of the eigenvectors, see Stefan Lafon's <a href="https://690cd646-a-62cb3a1a-s-sites.googlegroups.com/site/stefansresearchpapers/home/dissertation.pdf?attachauth=ANoY7cr1ahpFD_WRIwK_PDiIFpZAZeDlqNZjK2tkFfyybW2D2SEmtBT8NAVRJ2NeYkxlFDwccCsZyKGUFp7OLRW0RnV3LkyO1mw_CF36Pj26vBqY7wU_4Lj9BKCwnJv5heVHG4PGscqfWB7yiNpxR5-UcCuAZCW7cSUAbDluPN1A6HpHM0aZ2qYCr2drO40U2i9tx7C6i2fVMU6GcXuaabnbLQ8oXAhtKORx4PYDaAPhDgC2x7vn6-g%3D&attredirects=0">PhD dissertation</a>.

2. <b>Factorize the eigenvectors.</b> From step 1, we obtain a set of eigenvectors sorted by increasing eigenvalue. Using our result that product eigenvectors factorize into factor eigenvectors, for each eigenvector $\varphi_k$, we find the factorization $\varphi_i \times \varphi_j$ which is closest to $\varphi_k$. This “closeness” is measured by the absolute cosine similarity,<a href="#footnote1"><sup>1</sup></a>

    $$
    S(\varphi_k, \varphi_i\varphi_j) := \frac{|\langle \varphi_k , \varphi_i\varphi_j\rangle|}{||\varphi_k|| \cdot ||\varphi_i\varphi_j||}.
    $$

    This gives us a list $\mathcal{T}$ of triplets $(i,j,k)$, where each triplet contains our best approximation $\varphi_i \times \varphi_j \approx \varphi_k$.

3. <b>Group factor eigenvectors by manifold factor.</b> Define a weighted graph $H = (V, E, W)$ where $V$ is the set of unique factor eigenvectors in $\mathcal{T}$. The edge weights are given by the highest similarity score

    $$
    W_{ij} = \max_{(i,j,k) \in \mathcal{T}} S(\varphi_k, \varphi_i\varphi_j).
    $$

    Our problem now becomes one of separating the vertices into two groups, with higher priority given to separating vertices with high edge weights. Thus, this becomes formulated as a MAX-CUT problem. By using a MAX-CUT SDP solver with $H$ as the input, we can sort our factor eigenvectors into two bins that correspond to $\mathcal{M}_1$ and $\mathcal{M}_2$.

    <figure>
      <img src="" alt="Reformulating the problem of grouping factor eigenvectors by manifold factor as a MAX-CUT problem" style="width:100%">
      <figcaption>Figure 3. We can reformulate our problem of grouping factor eigenvectors by manifold factor as a MAX-CUT problem.</figcaption>
    </figure>

<h3>some fun results!</h3>

An interesting application of this method is in structural biology---specifically, applied to cryo-electron miscroscopy (cryo-EM) data. Cryo-EM is a microscopy technique that won <a href="https://pubmed.ncbi.nlm.nih.gov/29423601/#:~:text=The%202017%20Nobel%20Prize%20in%20Chemistry%20was%20awarded%20to%20Jacques,major%20achievements%20leading%20to%20the">the Nobel Prize in chemistry</a> and also played a role in many of the COVID-19 studies done over the past year. The main problem in 

<div class="footnotes">
<hr align="left" size="1">
<section id="footnote1"><sup>2</sup>We use the absolute cosine similarity rather than the signed cosine similarity because we can't distinguish between $\varphi_i$ and $-\varphi_i$.</section>

<section id="footnote2"><sup>2</sup>We use the absolute cosine similarity rather than the signed cosine similarity because we can't distinguish between $\varphi_i$ and $-\varphi_i$.</section>
</div>