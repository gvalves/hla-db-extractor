# hla-db-extractor

## Usage

```Sh
python3 main.py --dat "Input dat file path" --imgt "Output imgt file path" 
  --reader-strategy "Some strategy" --writer-strategy "Some strategy" 
  --reader-parser-strategy "Some strategy" --writer-parser-strategy "Some strategy"
  --from-imgt "Input imgt file to use as base for imgt output"
```

#### Reader Strategies

- *__default__*, not necessary to pass as argument
- *__quick__*, use more resource but take less time

#### Writer Strategies

- *__default__*, not necessary to pass as argument

#### Reader Parser Strategies

- *__default__*, not necessary to pass as argument

#### Writer Parser Strategies

- *__default__*, not necessary to pass as argument
- *__remove_empty_exon__*, remove hlas from imgt output that contains empty exons
