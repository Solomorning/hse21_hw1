# hse21_hw1
Создаём ссылки на все файлы:
>ls /usr/share/data-minor-bioinf/assembly/* | xargs -tI{} ln -s {}

Затем из них файлы в формате fastq:
>seqtk sample -s713 oil_R1.fastq 5000000 > paired_end_1.fastq  
>seqtk sample -s713 oil_R2.fastq 5000000 > paired_end_2.fastq  
>seqtk sample -s713 oilMP_S4_L001_R1_001.fastq 1500000 > MP_r1_001.fastq  
>seqtk sample -s713 oilMP_S4_L001_R2_001.fastq 1500000 > MP_r2_001.fastq  

Делаем fastqc и multiqc:
>mkdir fastqc  
>ls *.fastq | xargs -P 4 -tI{} fastqc -o fastqc {}  
>mkdir multiqc  
>multiqc -o multiqc fastqc  

Используя программу platanus укорачиваем контиги:  
>platanus_trim paired_end_1.fastq paired_end_2.fastq   
>platanus_internal_trim MP_r1_001.fastq MP_r2_001.fastq  

Собираем fastqc и составляем отчёт:  
>mkdir trimmed_fastqc  
>ls *.trimmed| xargs -P 4 -tI{} fastqc -o trimmed_fastqc {}  
>mkdir trimmed_multiqc  
>multiqc -o trimmed_multiqc trimmed_fastqc  

После этого можно сравнить получившиеся отчёты:  
![image](https://user-images.githubusercontent.com/93263163/139088717-a2593e49-0242-4133-a07b-82f941f6321e.png)
![image](https://user-images.githubusercontent.com/93263163/139088832-ab5d9727-9b5b-4307-8368-00173d23d7b9.png)
Уменьшилась длина последовательностей
![image](https://user-images.githubusercontent.com/93263163/139089304-38be0061-4496-476f-8f9a-47b429020dc2.png)
![image](https://user-images.githubusercontent.com/93263163/139089361-3a34c42b-e66b-4de2-bbbf-447a448ca1c5.png)
Улучшилась качество чтений
![image](https://user-images.githubusercontent.com/93263163/139089463-2fe044cc-7e01-4d3e-906d-15b6a5833aea.png)
![image](https://user-images.githubusercontent.com/93263163/139089594-14db31d7-9b9e-4872-a5d7-446b33dff620.png)
Удалены адаптеры

Собираем контиги, используя функцию assemble в platanus:
>platanus assemble -o Poil -t 8 -m 28 -f paired*.trimmed paired*.trimmed 2> assemble.log

Собираем скаффолды в platanus:
>platanus scaffold -o Poil -t 8 -c Poil_contig.fa -IP1 paired*.trimmed -OP2 MP*.trimmed 2> scaffold.log

После этого нужно выгрузить имеющиеся файлы и пропустить их через код src/main.py: 
![image](https://user-images.githubusercontent.com/93263163/139165820-50b2f102-db99-471e-bb90-b15ef3445d12.png)
Имеем следующие параметры для контигов:  
Total=3924999   
Longest=179307   
Shortest=87  
N50=55038  
И для скаффалдов:
Total=3875902  
Longest=3831852  
Shortest=102  
N50=3831852  
Количество гэпов=61  
Количество N=6062  

Закрываем имеющееся гэпы, используя функцию gap_close в platanus: 
>platanus gap_close -o Poil -t 8 -c  Poil_scaffold.fa -IP1 paired*.trimmed -OP2 MP*.trimmed 2> gapclose.log  

Записываем самый длинный scaffold(уже очищенный от гэпов) в отдельный .fna-файл:  
>echo scaffol_cov231 > _tmp.txt  
>seqtk subseq Poil_gapclosed.fa _tmp.txt > oil_genome.fna    
