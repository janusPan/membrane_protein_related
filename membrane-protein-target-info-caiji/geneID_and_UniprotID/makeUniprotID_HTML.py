def convert_uniprot_id_to_html(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            uniprot_id = line.strip()
            html_link = f'<a href="http://www.uniprot.org/uniprot/{uniprot_id}" >{uniprot_id}</a>'
            outfile.write(html_link + '\n')

# 使用示例
input_file = 'uniprotID.txt'
output_file = 'uniprotID_output.tsv'
convert_uniprot_id_to_html(input_file, output_file)