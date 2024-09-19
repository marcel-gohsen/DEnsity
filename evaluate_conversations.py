import click
import json

from evaluators.model import DEnsity
from utils.utils import load_tokenizer_and_reranker


def load_evaluator():
    lm_name = 'bert-base-uncased'
    model_path = './logs/dd/reranker.scl-temp0.1-coeff1.epoch10.lr5e-5/models/bestmodel.pth'
    mean_cov_pck_fname = "./results/pickle_save_path/dd/maha.ref-train.reranker-reranker.scl-temp0.1-coeff1.epoch10.lr5e-5.positive.pck"

    tokenizer, model = load_tokenizer_and_reranker(lm_name, model_path)
    evaluator = DEnsity(None, mean_cov_pck_fname, tokenizer, model)

    return evaluator


@click.command()
@click.option("--input-file", "-f", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--output-file", "-o", type=click.Path(exists=False, dir_okay=False), required=True)
def main(input_file, output_file):
    evaluator = load_evaluator()
    with open(input_file) as in_file:
        data = json.load(in_file)

    for conversation in data:
        utterances = [u["content"] for u in conversation["messages"]["predicted"] if u["role"] in {"user", "assistant"}]

        if "evaluation" not in conversation:
            conversation["evaluation"] = {"predicted": {}}

        if "predicted" not in conversation["evaluation"]:
            conversation["evaluation"]["predicted"] = {}

        score = evaluator.evaluate(utterances, is_turn_level=True)
        conversation["evaluation"]["predicted"]["density_last"] = float(score)

        score = evaluator.evaluate(utterances, is_turn_level=False)
        conversation["evaluation"]["predicted"]["density_avg"] = float(score)

    with open(output_file, "w+") as out_file:
        json.dump(data, out_file, indent=4)


if __name__ == '__main__':
    main()
