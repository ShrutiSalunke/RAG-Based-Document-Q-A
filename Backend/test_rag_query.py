import argparse
import os
import django 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup() 
from django.contrib.auth import get_user_model 
from documents.rag.query_engine import run_query
 
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question", help="The question to ask")
    parser.add_argument( "--user",  default=None, help="Username to run the query as (defaults to the first superuser found)", )
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()
 
    User = get_user_model()
    if args.user:
        user = User.objects.get(username=args.user)
    else:
        user = User.objects.filter(is_superuser=True).first()
        if user is None:
            raise SystemExit("No user found. Pass --user <username> or create a superuser first.")
 
    print(f"Running query as user: {user.username}")
    print(f"Question: {args.question}\n") 
    result = run_query(question=args.question, user=user, top_k=args.top_k) 
    print(f"Answerable: {result.answerable}")
    print(f"Retrieval latency: {result.retrieval_latency_ms} ms")
    print(f"Generation latency: {result.generation_latency_ms} ms")
    print(f"\nAnswer:\n{result.answer}\n") 
    if result.sources:
        print("Sources:")
        for s in result.sources:
            print(f"  - {s.document_name}, page {s.page_number}")
    else:
        print("Sources: (none -- question was not answerable from the corpus)")
 
 
if __name__ == "__main__":
    main()
