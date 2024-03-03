#!/bin/bash
#SBATCH -A research
#SBATCH -n 9
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH -w gnode091
#SBATCH --mem-per-cpu=2G
#SBATCH --time=4-00:00:00
#SBATCH --output=/home2/aditya.pavani/rsai_balu/project/visogender/logs/downloader.log
#SBATCH --mail-user lakshmipathi.balaji@research.iiit.ac.in
#SBATCH --mail-type ALL

cd /home2/aditya.pavani/rsai_balu/project/visogender
source ~/.miniconda3/envs/visogender/bin/activate
python data_downloader.py