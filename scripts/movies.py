from neo4j import GraphDatabase
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# Configure Neo4j database connection
uri = "bolt://localhost:7687"
user = "neo4j"
password = "***"  # Change to your password
driver = GraphDatabase.driver(uri, auth=(user, password))

# Test query: Find actors who appeared in 'The Matrix'
query_simple = """
MATCH (p:Person)-[:ACTED_IN]->(m:Movie {title: 'The Matrix'})
RETURN p.name
"""

# Complex query: Find if two actors have collaborated in a movie
query_complex = """
MATCH (p1:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(p2:Person)
WHERE p1.name <> p2.name
RETURN DISTINCT p1.name, p2.name
"""

# Path query: Find collaboration chain starting from Keanu Reeves
query_path = """
MATCH p=shortestPath((p1:Person {name: 'Keanu Reeves'})-[:ACTED_IN*]-(p2:Person))
WHERE p1 <> p2
RETURN p2.name, length(p)
"""

# Execute a query
def run_query(tx, query):
    tx.run(query)

def execute_single_query(query):
    with driver.session() as session:
        session.execute_read(run_query, query)

# Single-thread query performance test
def single_thread_test(query, num_queries=1000):
    start = time.time()
    for _ in range(num_queries):
        execute_single_query(query)
    end = time.time()
    total_time = end - start
    print(f"Single-thread test ({num_queries} queries) completed.")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per query: {total_time / num_queries:.5f} seconds")

# Multi-thread concurrent query performance test
def multi_thread_test(query, num_queries=1000, num_threads=10):
    start = time.time()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(execute_single_query, query) for _ in range(num_queries)]
        for future in futures:
            future.result()
    end = time.time()
    total_time = end - start
    print(f"Multi-thread test ({num_queries} queries with {num_threads} threads) completed.")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per query: {total_time / num_queries:.5f} seconds")

# Insert performance test: Insert data into the database
def insert_test(num_inserts=1000):
    with driver.session() as session:
        start = time.time()
        for i in range(num_inserts):
            session.run(
                "MERGE (p:Person {name: $name})",  # Using MERGE instead of CREATE
                name=f"Person_{i}"
            )
        end = time.time()
    total_time = end - start
    print(f"Insert test ({num_inserts} inserts) completed.")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per insert: {total_time / num_inserts:.5f} seconds")

# Run all tests
def run_all_tests():
    # Single-thread test: Simple query
    print("Running single-thread test for simple query...")
    single_thread_test(query_simple, 1000)

    # Single-thread test: Complex query
    print("\nRunning single-thread test for complex query...")
    single_thread_test(query_complex, 500)

    # Single-thread test: Path query
    print("\nRunning single-thread test for path query...")
    single_thread_test(query_path, 500)

    # Multi-thread test: Simple query
    print("\nRunning multi-thread test for simple query...")
    multi_thread_test(query_simple, 1000, 10)

    # Multi-thread test: Complex query
    print("\nRunning multi-thread test for complex query...")
    multi_thread_test(query_complex, 500, 10)

    # Insert performance test
    print("\nRunning insert performance test...")
    insert_test(1000)

# Execute benchmark tests
if __name__ == "__main__":
    run_all_tests()
    driver.close()