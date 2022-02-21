#!/usr/bin/python3
import pypinyin
import itertools

class PinyinException(Exception): pass

printed = set()

def strict(x):
  for i in x:
    if i not in printed:
      printed.add(i)
      print(f"No pinyin for character {i}")
  raise PinyinException(f"No pinyin for character {x}")

pypinyin.load_single_dict({
  # ord("一"): "h", # 横
  # ord("丨"): "s", # 竖
  # ord("丶"): "d", # 点
  # ord("乀"): "n", # 捺
  # ord("丿"): "p", # 撇

  # ord("一"): "yi",
  # ord("丨"): "gun",
  # ord("丶"): "zhu",
  # ord("乀"): "fu",
  # ord("丿"): "pie",
  # ord("乁"): "yi,ji",
  # ord("乙"): "yi",
  # ord("乚"): "hao,yi",
  # ord("乛"): "yi",
  # ord("亅"): "jue",

  # ㇆, 龴, ⺆, , 龹, ㇉, 龷, 𠃋, 𡕩, 𠃑
})

with open("chaizi/chaizi-jt.txt") as i, open("chaizi/chaizi-ft.txt") as i2, open("chaizi.dict.yaml", "w") as o:
  o.write("""---
name: chaizi
version: "20170901"
...
""")
  for line in itertools.chain(i.readlines(), i2.readlines()):
    if "□" in line:
      continue
    char, *methods = line[:-1].split("\t")
    outputs = set()
    for method in methods:
      try:
        pinyins = pypinyin.pinyin(method.replace(" ", ""), style=pypinyin.NORMAL, heteronym=True, errors=strict)
      except PinyinException:
        continue
      # for permutation in itertools.permutations(pinyins):
      for parts in itertools.product(*pinyins):
        parts = " ".join(parts)
        output = "\t".join([char, parts])
        if output not in outputs:
          outputs.add(output)
          print(output, file=o)
