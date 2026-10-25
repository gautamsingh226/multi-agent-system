from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def  run_research_pipeline(topic : str) -> dict:
    state={}
    
    #step 1 - search agent working 
    print("\n" + "="*50)
    print("step 1 - search agent is working.............")
    print("="*50 + "\n")
    
    seach_agent = build_search_agent()
    search_results = seach_agent.invoke({
        "messages":[("user",f"find recent and reliable information on the topic: {topic}")],
    })
    state["search_results"] = search_results['messages'][-1].content
    print("\n" + "seatch results:",state["search_results"])
    
    
    #step2 - reader agent working 
    print("\n" + "="*50)
    print("step 2 - reader agent is scraping top resources.............")
    print("="*50 + "\n")
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    state['scraped_content'] = reader_result['messages'][-1].content
    print("\nscraped content:",state["scraped_content"])
    
    
    #step 3 - writer chain
    print("\n" + "="*50)
    print("step 3 - writer is drafting  the final report.............")
    print("="*50 + "\n")  
    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = state['report'] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    print("\nfinal report:",state["report"])
    
    
    
    #critic report
    print("\n" + "="*50)
    print("step 4 - critic is evaluating the report.............")
    print("="*50 + "\n")
    
    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })
    print("\n criritc feedback \n:",state["feedback"])
    
    return state

if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    run_research_pipeline(topic)