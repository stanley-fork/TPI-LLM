import argparse
import torch.multiprocessing as mp
from run_llama import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # necessary arguments
    parser.add_argument("--model_type", default=None, type=str, required=True)
    parser.add_argument("--model_path", default=None, type=str, required=True)
    parser.add_argument("--world_size", default=None, type=int, required=True)
    parser.add_argument("--master_ip", type=str, default="127.0.0.1")
    parser.add_argument("--master_port", type=int, default=29500, help="Communication port.")
    # for weight file synchronization
    parser.add_argument("--file_port", type=int, default=29600, help="File server port.")
    parser.add_argument("--force_download", action="store_true", help="Force download sliced model files.")
    # for llm inference
    parser.add_argument("--prompt", type=str, default="")
    parser.add_argument("--length", type=int, default=20)
    parser.add_argument("--prefix", type=str, default="", help="Text added prior to input.")
    parser.add_argument("--use_gpu", action="store_true", help="Whether to use gpu, default to use cpu.")
    parser.add_argument("--split_bin", action="store_true", help="Whether to split the model file.")
    parser.add_argument("--save_dir", type=str, default="split", help="Directory to save split models.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--k", type=int, default=0)
    parser.add_argument("--p", type=float, default=0.9)
    # for memory schedule
    parser.add_argument("--disable_memory_schedule", action="store_true")
    parser.add_argument("--memory_window", type=int, default=2,
                        help="Memory window size, should be at least 2.")
    args = parser.parse_args()

    processes = []
    mp.set_start_method("spawn")
    for rank in range(args.world_size):
        p = mp.Process(target=main, args=(rank, args))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
