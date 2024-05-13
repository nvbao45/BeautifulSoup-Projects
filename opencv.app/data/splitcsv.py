chunk_size = 1000

def write_chunk(part, lines):
    with open(str(part) + '.csv', 'w', encoding='utf-8') as f_out:
        f_out.write(header)
        f_out.writelines(lines)
        
with open("openvc.csv", "r", encoding='utf-8') as f:
    count = 0
    header = f.readline()
    lines = []
    for line in f:
        count += 1
        lines.append(line)
        if count % chunk_size == 0:
            write_chunk(count // chunk_size, lines)
            lines = []
    if len(lines) > 0:
        write_chunk((count // chunk_size) + 1, lines)