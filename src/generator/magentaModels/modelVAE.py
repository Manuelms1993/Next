import note_seq
import logging
from magenta.models.music_vae import configs
from magenta.models.music_vae.trained_model import TrainedModel
from utils.constant import Constants
import sys

# https://github.com/magenta/magenta/tree/master/magenta/models/music_vae#pre-trained-checkpoints
# https://github.com/magenta/magenta-js/blob/master/music/checkpoints/README.md

def getTrainedModelVAE(config_map_model, batch_size = 8, own=False):

    chkpnt = None

    if (not own):
        if (config_map_model == 'groovae_4bar'):
            chkpnt = Constants.MAIN_PATH + '/content/model.ckpt-2721'
        if (config_map_model == 'cat-mel_2bar_big'):
            chkpnt = Constants.MAIN_PATH + '/content/cat-mel_2bar_big.ckpt'
        if (config_map_model == 'hierdec-mel_16bar'):
            chkpnt = Constants.MAIN_PATH + '/content/hierdec-mel_16bar.ckpt'
        if (config_map_model == 'nade-drums_2bar_full'):
            chkpnt = Constants.MAIN_PATH + '/content/nade-drums_2bar_full.ckpt'
        if (config_map_model == 'groovae_2bar_add_closed_hh'):
            chkpnt = Constants.MAIN_PATH + '/content/model.ckpt-4126'
        if (config_map_model == 'groovae_2bar_humanize'):
            chkpnt = Constants.MAIN_PATH + '/content/model.ckpt-3061'
        if (config_map_model == 'hierdec-trio_16bar'):
            chkpnt = Constants.MAIN_PATH + '/content/hierdec-trio_16bar.ckpt'
    else:
        chkpnt = Constants.MAIN_PATH + "/" + config_map_model
        config_map_model = 'cat-mel_2bar_small'

    if (chkpnt == None):
        logging.error("Model Not Found: " + config_map_model)
        sys.exit(1)

    logging.info("Loading " + config_map_model + "in checkpoint: " + chkpnt)
    return TrainedModel(
        configs.CONFIG_MAP[config_map_model],
        batch_size=batch_size,
        checkpoint_dir_or_path=chkpnt)

def generateVAE(model, n, steps, temperature):

    generated_sequences = model.sample(n = n, length = steps, temperature = temperature)
    return generated_sequences