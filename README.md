![](https://github.com/antoinedang/McHacks2023/blob/8e9e23ee4ead5c12c74a4658331f11f2f6dad2f2/server/static/assets/img/portfolio/part4_mobile.gif)

# McHacks2023
Project repository for McGill Hackathon for January 2023. Team of 4: Ben Hepditch, Elie Dimitri-Abdo, Rudi Kischer, Antoine Dangeard

## Inspiration
As developers, we were on a mission to create something truly extraordinary. Something that would change the way people approach to fashion and make getting dressed in the morning an easier and more enjoyable experience.

Introducing Rate My Fit, our revolutionary AI software program that rates people's outfits based on color coordination, mood/aesthetic, appropriateness for the current weather, and the combination of complementary textures. We wanted to create a tool that not only enhances people's fashion sense but also helps them make the best outfit choices for any occasion and weather.

## What it does
We used cutting-edge image recognition technology and machine learning algorithms to train our program to understand the nuances of fashion and personal style. It can analyze an individual's outfit and give instant feedback on how to make it even better.

We are passionate about our technology and the impact it has on people's lives. We believe that our AI outfit rating program will empower individuals to make confident and stylish fashion choices, regardless of their body type, skin tone, or personal style.

## How we built it
Building our AI outfit rating software was a challenging and exciting journey. Our goal was to create a program that was not only accurate and efficient but also user-friendly and visually appealing.

We began by selecting the appropriate technology stack for our project. We chose to use Python and Flask for the back-end, JavaScript, CSS, and HTML for the front-end, and a state-of-the-art computer vision architecture in Python for the image recognition component.

To train our computer vision model, we collected a dataset of over 200,000 images of various outfits. We carefully curated the dataset to ensure a diverse representation of styles, body types, and occasions. Using this dataset, we were able to train our model to accurately recognize and analyze different aspects of an outfit such as color coordination, mood/aesthetic, appropriateness for the current weather, and the combination of complementary textures.

Once the model was trained, we integrated it into our web application using Flask. The front-end team used JavaScript, CSS, and HTML to create a visually appealing and user-friendly interface. We also added a weather API to the software to provide real-time information on the current weather and make the rating even more accurate.

The final product is a powerful yet easy-to-use software that can analyze an individual's outfit and provide instant feedback on how to make it even better. We are proud of the technology we used and the impact it has on people's lives.

## Challenges we ran into

- **Cleaning and organizing the dataset**: With over 200,000 images to sift through, it was a daunting task to ensure that the images were high quality, diverse and appropriately labeled. It took a lot of time and effort to make sure the dataset was ready for training.

- **Building the complex JavaScript UI**: We wanted to create a visually appealing and user-friendly interface that would make it easy for users to interact with the software. However, this required a lot of attention to detail and testing to ensure that everything worked smoothly and looked good on various devices.

- **Creating the back-end processing for the analytics**: We needed to create an efficient pipeline to process the outfit ratings in real-time and provide instant feedback to the users. This required a lot of experimentation and testing to get the right balance between speed and accuracy.

- **Training the model** in PyTorch on a GPU: We had to optimize the training process and make sure the model was ready in time for the project submission. It was a race against time to get everything done before the deadline but with a lot of hard work, we were able to meet the deadline.


## Accomplishments that we're proud of
We're most proud of being able to train and deploy our own custom computer vision model. This is something we've all had the ambition to take on for quite a while but were always intimidated by the daunting task that training a neural network entails. Additionally, we're proud of building a full stack web app which is compatible with bot mobile OS and desktop use. 

Overall, building this software was a challenging but rewarding experience. We learned a lot and pushed ourselves to new limits in order to deliver a product that we are truly proud of.

## What we learned
**Using Cuda to train PyTorch models can be very frustrating!** (Documentation is lacking). Also, building tests for the back-end to validate the quality of the ratings and the overall user experience was fun but more intensive than we envisioned.

## What's next for Rate My Fit
- Adding a live fit detection feature.
- Configuring a database to allow users to save their outfits for future reference.
- Add more analytical functionalities.
- Be able to recognize a wider range of clothing styles and garments.
