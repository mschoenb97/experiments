Here is the experiment code! Here is what you need to do to get this running.

1. Rewrite `train_model_complex` in the `run_experiments.py` 
file. If you need new configurable inputs, let me know. Make sure that the outputs
are of the same format. 
  - You should be able to copy all of the `argument pre-processing` code (as described in the comments).
  - Be sure to `deepcopy` the quantizer every time you pass it into a layer. These quantizers have to know
  the shape of the input (this is done in the `build` step of `QConv2DClean`)
  - Do not quantize the activations.
2. In my model, I quantize all weights except for the final dense layer, i.e. 
  the last two elements of the weights list. If this is NOT the case for you, please
  let me know and I can make this configurable.
  - You'll notice that this is the only place that I use the `straight_initializer`. 
  This just ensures that the weights are initialized without any remapping. Be
  sure to do the same for any non-quantized layers. 
3. The parameters for the run are located in the config. We may need to meet to 
  discuss what all the config options mean. For any new run, you should
  create a new `<directory>`, put a config in that directory, and run `python run_experiments.py <directory>`.
  Results for each model are cached, as well as all images. The final metrics are
  in `results.json`. 
4. At the moment there is no "delayed start" like the one we discussed before.
  Instead we're using a warmup schedule, which gives good results. 
5. I've run into some CPU memory issues with this code, primarily due to the change point calculations.
  I only got this to work with I used a t3.2xlarge instance on AWS (see [here](https://aws.amazon.com/ec2/instance-types/t3/)).