function emoji_lookup(input, env)
  input_text = env.engine.context.input
  if #input_text > 1 and input_text:byte(1) == 96 then -- input_text:sub(1, 1) == "`"
    for cand in input:iter() do
      index = cand.text:find("|")
      text = cand.text:sub(1, index - 1)
      comment = cand.text:sub(index + 1)
      yield(Candidate(cand.type, cand.start, cand._end, text, comment))
    end
  else
    for cand in input:iter() do
      yield(cand)
    end
  end
end

function match(comment, preedit)
  --[[ 等价Python代码
  for cstr, pstr in zip(comment.split(), preedit.split()):
    if not cstr.startswith(pstr):
      return False
  return True ]]
  cend = 0
  pend = 0
  while cend ~= nil and pend ~= nil do
    cstart = cend + 1
    pstart = pend + 1
    cend = comment:find(" ", cstart)
    pend = preedit:find(" ", pstart)
    if cend == nil then
      cstr = comment:sub(cstart)
    else
      cstr = comment:sub(cstart, cend - 1)
    end
    if pend == nil then
      pstr = preedit:sub(pstart)
    else
      pstr = preedit:sub(pstart, pend - 1)
    end
    if cstr:sub(1, #pstr) ~= pstr then
      return false
    end
  end
  return true
end

function fuzz_fix(input, env)
  for cand in input:iter() do
    type = cand.type
    if type == "simplified" then -- 抹去 emoji 的注释
      yield(Candidate(type, cand.start, cand._end, cand.text, ""))
    elseif type == "phrase" or type == "user_phrase" then
      if match(cand.comment, cand.preedit) then
        cand.comment = "" -- 如果是简拼而非模糊音，抹去注释
      end
      yield(cand)
    else -- 只对 script_translator 生效
      yield(cand)
    end
  end
end
