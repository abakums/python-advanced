FROM ubuntu:22.04

RUN apt-get update && apt-get install -y texlive-latex-recommended python3 python3-pip
RUN pip install -i https://test.pypi.org/simple/ my-latex-package==0.0.1

COPY main.py /app/main.py
COPY images /app/images

WORKDIR /app

CMD python3 main.py && pdflatex output.tex && mv output.pdf /output/output.pdf
