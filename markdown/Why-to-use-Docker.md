# Why to run tax.co in Docker

You don't have to, but it's easier and safer.

tax.co is written in Python using Numpy, Scipy and Pandas. 
The libraries used will surely expand. 
So far they are all included in a vanilla install of Anaconda; 
however, that might not always be true. 
If you want to work more than necessary, 
you could stay on top of all those new libraries yourself. 
However, we will be maintaining a Docker image of Anaconda with every required library already installed.
