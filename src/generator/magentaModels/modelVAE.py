import note_seq
import logging
from magenta.models.music_vae import configs
from magenta.models.music_vae.trained_model import TrainedModel
from utils.constant import Constants

# https://github.com/magenta/magenta/tree/master/magenta/models/music_vae#pre-trained-checkpoints

def getTrainedModelVAE(config_map_model, batch_size = 8):

    chkpnt = None
    if (config_map_model == 'groovae_4bar'):
        chkpnt = Constants.MAIN_PATH + '/content/model.ckpt-2721'
    if (config_map_model == 'cat-mel_2bar_big'):
        chkpnt = Constants.MAIN_PATH + '/content/cat-mel_2bar_big.ckpt'
    if (config_map_model == 'hierdec-mel_16bar'):
        chkpnt = Constants.MAIN_PATH + '/content/hierdec-mel_16bar.ckpt'

    if (chkpnt == None):
        logging.error("Model Not Found: " + config_map_model)

    logging.info("Loading " + config_map_model + "in checkpoint: " + chkpnt)
    return TrainedModel(
        configs.CONFIG_MAP[config_map_model],
        batch_size=batch_size,
        checkpoint_dir_or_path=chkpnt)

def generateVAE(model, n, steps, temperature):

    generated_sequences = model.sample(n = n, length = steps, temperature = temperature)
    return generated_sequences