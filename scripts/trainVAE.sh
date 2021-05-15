project="/Users/manuelmontero/PycharmProjects/NEXT"

name="deadmau5"
midi_files_path="/resources/mid/ManuelMontero/Deadmau5"
INPUT_DIRECTORY=$project$midi_files_path
OUTPUT_DS_DIRECTORY=$project"/tmp/notesequences.tfrecord"
modelDir=$project"/model/"$name"/"
model="cat-mel_2bar_small"

echo "midi_files_path: "$midi_files_path
echo "INPUT_DIRECTORY: "$INPUT_DIRECTORY
echo "OUTPUT_DS_DIRECTORY: "$OUTPUT_DS_DIRECTORY
echo "modelDir: "$modelDir
echo "name: "$name

convert_dir_to_note_sequences --input_dir=$INPUT_DIRECTORY --output_file=$OUTPUT_DS_DIRECTORY --recursive

music_vae_train \
--config=$model \
--run_dir=$modelDir \
--mode=train \
--examples_path=$OUTPUT_DS_DIRECTORY
--hparams=batch_size=512,learning_rate=0.001

touch $modelDir"/"model

#HParams(
#            batch_size=512,
#            max_seq_len=32,  # 2 bars w/ 16 steps per bar
#            z_size=256,
#            enc_rnn_size=[512],
#            dec_rnn_size=[256, 256],
#            free_bits=0,
#            max_beta=0.2,
#            beta_rate=0.99999,
#            sampling_schedule='inverse_sigmoid',
#            sampling_rate=1000,
#        )),