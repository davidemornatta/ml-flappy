# ml-flappy

My first try with TFLearn and OpenAI gym.
The goal is to create a "flappy bird"-like game and train it using Deep Learning. The game has been created using Pygame.

I developed a custom environment for OpenAI gym called "FlappyEnv", that handles the mechanics of the game and is ready to be studied by the neural network.
The chosen neural network is made up of 5 nodes and trained with Linear Regression.

In the current state the bird is able to reach the first pipe and, sometimes, overcome it and then lose.
This is a very basic training of the model, so this result is not really remarkable to see, but it still (almost) doubles the initial scores.
