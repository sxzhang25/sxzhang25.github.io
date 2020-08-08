---
layout: post
title: "constructing depth in 3d photos"
date: 2020-08-12
refs:
  - >
    Shih, Meng-Li, et al. "3D Photography using Context-aware Layered Depth Inpainting." <i>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition.</i> 2020.
  - >
    Shade, Jonathan, et al. "Layered depth images." <i>Proceedings of the 25th annual conference on Computer graphics and interactive techniques.</i> 1998.
  - >
    Xiong, Wei, et al. "Foreground-aware image inpainting." <i>Proceedings of the IEEE conference on computer vision and pattern recognition.</i> 2019.
---

The first 3D photo I saw was on Facebook a few years back. I was swiping through my feed, when I suddenly noticing an extra, unfamiliar movement as I scrolled past an image of a cat (of course). It turns out that the motion was from the image itself, and there was a small icon overlaid on top of the image that had a moving mouse symbol. It only took a second of interacting with the photo for me to figure out that this was a 2D image with an additional dimension of depth integrated in some way. Moving the mouse around the photo allowed me to see the cat from a slightly different angle, as if the position of the mouse represented the position of my head in the space in which the cat lived.

<!--excerpt-->

I thought the idea of a 3D photo was neat, but back then they weren't that impressive yet. At the time, the features only worked on portrait mode images, in which the background was already heavily blurred. Earlier this year, Facebook released a new 3D photo feature that included support for <i>any</i> kind of photo, and the experience of "moving around" in a 3D photo has become much cleaner and more natural. However, there are still parts of the 3D photo which look very unnatural. Namely, if you move the view far enough from the original image view, you can see a cutout of the main subject in the background which has been filled with a heavily blurred "guess" of what the background behind the subject should be. Recently, I came across a paper, <a href="https://arxiv.org/pdf/2004.04727.pdf"><i>3D Photography using Context-aware Layered Depth Inpainting</i></a> by Shih et al., which addresses ways of mitigating those artifacts.

<h3>how do you create a 3D photo?</h3>

To answer this question, we have to start with a discussion on perspective. Perspective is a huge foundational concept in computer vision and camera technology, and having gone through middle school art class I know that perspective is easy to understand, but hard to speak.<a href="#footnote1"><sup>1</sup></a> In a 3D photo, perspective is the name of the game. The dimension that separates a normal 2D photo from the 3D photo is depth, and we develop the understanding of depth through how the objects we look at move as we "move" our own head (or mouse, or phone). Since perceived distances decrease as depth increases, objects that are farther away appear to move more slowly or subtly than objects that are closer. 

An extremely basic and somewhat successful way of simulating 3D motion is to simply warp parts of the image. An example of this is the <a href="">Motion Portrait app</a>, which has been around for a while now. The app basically takes a portrait of someone's face, places anchors on their eyes and mouth, and warps those anchors and the entire head so that the person looks like they are moving their head around and blinking. It's pretty crude, but it works well enough to produce a very shallow depth of field effect.

<figure>
  <img src="https://github.com/sxzhang25/sxzhang25.github.io/raw/master/imgs/2020-08-12-fig1a.JPG" alt="Original image" style="width:33%">
  <img src="https://github.com/sxzhang25/sxzhang25.github.io/raw/master/imgs/2020-08-12-fig1b.PNG" alt="Image with anchored facial features" style="width:33%">
  <img src="https://github.com/sxzhang25/sxzhang25.github.io/raw/master/imgs/2020-08-12-fig1c.gif" alt="Motion portrait" style="width:33%">
  <figcaption>Figure 1. How a Motion Potrait works. (Left) The original image. (Middle) First, we identify the eyes and the mouth. (Right) Then, we simply drag groups of pixels around to create the illusion of new views. I used an artificially generated photo of a person!</figcaption>
</figure>

The limitations of this method are immediately clear. While they might be able to create the basic illustion of movement out of a single image, it's pretty much impossible to make these new views realistic from only one sample. The difference between areas that are being warped and areas that are not being warped is pretty obvious, and the space between warped and unwarped regions is weirdly smudged or dragged out. You can definitely tell that the motion is being derived from warping a single static image.

But this idea is slightly different from what we want--instead of the object in the image moving as if it were 3D, we want to our own physical motion to change the view of the photo so that it continues to <i>look</i> still, but from a different point of view. Unlike in the the Motion Portrait, our line of sight is supposed to be fixed on one central object in the image, and the depth is simulated by keeping the foreground object <i>fixed</i> while moving the background of the image in a way that creates the illusion of perspective.

<h3>generating 3d from a single image</h3>

The biggest obstacle of generating a realistic 3D photo is filling in background objects that appear as we move around the subject. In the original image, the subject occludes a certain portion of the background. But as we move to the right, perspective dictates that some of these occluded parts should become visible, while areas of the background on the left of the subject which we could previously see now become occluded. But how do we fill in these newly visible parts of the image, when we never had any information about them to begin with?

<figure>
  <img src="https://github.com/sxzhang25/sxzhang25.github.io/raw/master/imgs/2020-08-12-fig2.png" alt="Perspective demonstration" style="width:100%">
  <figcaption>Figure 2. Missing information in new views. Black represents the area that the original image (left) does not show. </figcaption>
</figure>

At this point, we can pursue two different approaches. One way is to use machine learning models to predict a suitable texture to fill in the new hole that we have created, using the context of the existing background. The other way is pretty straightforwards--simply take more pictures. There are a lot of interesting ways to accomplish this using multiple images and the results are pretty amazing (see work by researchers at UC Berkeley <a href="https://www.matthewtancik.com/nerf">here</a> and <a href="https://people.eecs.berkeley.edu/~bmild/llff/">here</a>). In the case of Facebook's 3D photo feature, a single-image approach is more appropriate since a user might not have multiple views of the image they captured. This is also the limitation assumed by Shih et al. in their work, and the amount of information they managed to extrapolate from a single image is extremely amazing.

<h3>layered depth images</h3>

The final image object that the Shih et al. create is actually not a typical fully-connected grid of pixels. Instead, the authors use what is called a <i>layered depth image</i>, or an LDI. This concept was introduced by Jonathan Shade et al. in their 1998 paper <a href="https://dl.acm.org/doi/pdf/10.1145/280814.280882?casa_token=0eXnnnA7wtQAAAAA:s2fxkxUJUvx2NbAYFj8EYMNoQml-bosvWMElGMH0E0QevLca1sJuGt-W5qekgLJhK0z0FspOaE8k"><i>Layered Depth Images</i></a>. A normal image is typically stored as an array of pixels, where each pixel contains an array of values corresponding to RGB and potentially other information. The analogous unit to a pixel in an LDI is a Layered Depth Pixel (LDP). Each LDP stores multiple Depth Pixels (DPs), which hold RGBA, depth, and splat<a href="#footnote2"><sup>2</sup></a> information. An LDP can store varrays of DPs of varying lengths, so they easily represent the different "layers" of depth that are present in an image scene.

As discussed by Shade et al., the LDI has the advantage of being able to supply information for recreating parallax effects as well as originally occluded regions. This representation is also sparser than other layer-based representations, since it does not store a fixed amount of information at each LDP. Shih et al. also mention that this representation can be easily converted into a lightweight mesh, which makes sense because the number of layers at each Layer Pixel already creates some sort of topographical depth structure. In my understanding, the LDI is like a 3D printed object compared to other layer-based representations, which might align more closely to the block of plastic that the 3D printer starts out with.

<h3>recreating what we can't see</h3>

The first step in constructing an LDI is to obtain a suitable depth map of the image. The step in this part that I thought was interesting was the authors' choice to use a bilateral median filter on the depth map, in order to sharpen the edges (so that discrete discontinuities in depth could be emphasized). I learned about this filter pretty early on in computer graphics, but at the time the only use case I could come up for it was to apply a Gaussian blur on an image while preserving important contours. Using this filter to smooth out the depth map and sharpen edges is a neat trick that I will definitely keep in mind. Once this is done, discontinuities are identified and stored as "depth edges," which is where inpainting will occur.

Inpainting actually occurs in three different components: color, depth, and depth edges. When I first thought about the inpainting problem, I only ever considered color--to me, a texture was just a function mapping position to color. However, it does make sense to consider depth during inpainting as well, because occluded objects may not necessarily have the same depth position, and any new view must accurately synthesize the positions of these various unseen depths. Depth edges, on the other hand, are more analogous to hidden contours, marking the occluded boundaries between different degrees of depth.

Generating the actual hidden contours and background texture is something covered deeply in <a href="https://arxiv.org/pdf/1901.05945.pdf">this paper</a> by Xiong et al., but essentially both contour and image completion are accomplished using GAN architectures.

<h3>how does it hold up?</h3>
It turns out that the current iteration of 3D photos that Facebook has on their app is mostly based on depth estimation, and doesn't really do much inpainting. Depth estimation is a problem that one of my professors has studied extensively, and I had the chance to learn a lot about last semester. I'm guessing that this inpainting pipeline either takes too long to run on a mobile device, the simpler blurring method produces more consistent results, or maybe a version of the feature that integrates this algorithm just hasn't been implemented yet. In any case, I thought I might still share some of my rown 3D photo results.

<figure>
  <img src="https://github.com/sxzhang25/sxzhang25.github.io/raw/master/imgs/2020-08-12-fig3a.gif" alt="Amsterdam 2019" style="width:33%">
  <img src="https://github.com/sxzhang25/sxzhang25.github.io/raw/master/imgs/2020-08-12-fig3b.gif" alt="Key West Florida 2019" style="width:33%">
  <img src="https://github.com/sxzhang25/sxzhang25.github.io/raw/master/imgs/2020-08-12-fig3c.gif" alt="A tea kettle" style="width:33%">
  <figcaption>Figure 3. Examples of 3D photos made in the Facebook app. </figcaption>
</figure>

The most successful examples typically contained a clear subject with a non-reflective texture, coupled with a simple background and minimal complexities (occlusions, random textures, etc.). This is probably a majority of photos that get processed. There are, however, understandably difficult cases in which the depth estimation fails. Finer details such as hair are hard to segment individually, as you can see from the leftmost image in Figure 3. This is not surprising, since this happens in artificial portrait modes on smartphone cameras, and is a relatively hard case for image segmentation too. The tea kettle image in Figure 3 is one such instance. The specular reflections and rust on the surface of tea kettle caused the reflective portions of the surface to get segmented into a different depth segment than the rest of the tea kettle. Even more interesting was the warping of the right part of the handle--in this case, the bottom of the handle seemed to get locked in with the background depth, while the top of the handle stayed consistent with the rest of the tea kettle. I'd be really interested in such failure cases because this is not behavior I would expect at all, and understanding where it comes from might help clarify the inner workings of the depth estimation net. In the end though, I am super impressed by the results.

The paper's <a href="https://shihmengli.github.io/3D-Photo-Inpainting/">web demo</a> shows some results from the algorithm by Shih et al. I highly recommend checking them out--they have a much wider range of perspectives than the 3D photos, and the inpainting is nearly seamless. It's still obvious that the photos are artificially 3D, but besides the fact that the shot is completely still while having depth, it's much harder to pinpoint exactly what makes them look processed.

<h3>other applications of inpainting</h3>

Apart from creating 3D photos, inpainting is hugely relevant to creative technology softwares. As a long-time user of Photoshop, I've used their content-aware fill tool hundreds of times. I've also seen it fail in some cases, and as Photoshop has evolved from CS3 to CS6 their content-aware tools have gotten noticeably better. Last year, a content-aware tool was also <a href="https://www.youtube.com/watch?time_continue=68&v=QBq6ZJBHABU&feature=emb_logo">introduced in After Effects</a> for removing moving subjects in videos.<a href="#footnote3"><sup>3</sup></a> For videos though, I've read that the results really depend on good manual tracking inputs of a subject over keyframes and a good selection mask, although it takes a long time to run. The feature also seems to fail when the background contains complicated textures, such as grass, sand, or artificial structures and occlusions. This isn't surprising, since it's much harder to maintain inpainting consistency across many frames in a video. Even if there are slight inconsistencies between frames, a viewer can easily detect them. Also, sometimes the background being occluded by a subject in one frame is not occluded anymore in a different frame, and we would want the generated fill to be as close as possible from the ground truth in this case, which seems pretty difficult. I wonder if it would be possible to use some sort of copy and paste of background textures in corresponding locations between frames for these cases, adjusted by some homography that accounts for any possible camera movements between the frames.

There's a lot of great computer vision work etched into the foundations of creative tech software that I have always wanted to deep dive into. This is an area I'm extremely interested in learning more about, and I'll be sure to look out for other related papers in the future.

<div class="footnotes">
<hr align="left" size="1">
<section id="footnote1"><sup>1</sup>What I mean by this is: intermediate-level speakers of a language are often good at listening and understanding others speaking the language, but much less fluent at speaking the language themselves. When dealing with perspective, many people can <i>understand</i> perspective--they can easily identify when the perspective of a painting or image looks off or wrong--but it can be much harder for them to come up with a view for a given perspective on their own. A simple exercise is this: try drawing a 3D lowercase letter 'e' from 8 different views (e.g. you are looking at the 'e' from above, you are looking at the 'e' from below, you are looking at the 'e' from the right, etc.). Drawing the proper extrusions to simulate these views is something that many people struggle with.</section>

<section id="footnote2"><sup>2</sup><i>Splatting</i> is a volume rendering technique in which a volume element is thrown at the image plane (imagine a snowball going SPLAT! onto a brick wall and flattening out like a pancake). The properties of this disc-shaped splat are weighted radially using a Gaussian distribution. This technique allows for faster rendering, but reduces the quality of the final image.</section>
</div>