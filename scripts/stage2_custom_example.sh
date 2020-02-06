#!/bin/sh

./macro/stagex.py \
      inputs/dayabay_p19a_test_subs/**.root \
      -o output/test_stagex \
      --function1 stage1_test \
      --stage 1 \
      --cfg IbdSel/static/configs/config.nominal.txt
