

# Update ptdX files from form Inputs
def update_elements(parent_element, parent_tag, updates):
    """Updates specific XML elements inside <A_002> or <I_002>."""
    parent = parent_element.find(parent_tag)
    updated = False

    # Define the elements that we need to update
    elements_to_update = [
        "Owner", "City", "Pipe_Use",  # Inside <A_002>
        "Customer", "Project", "WorkOrder", "Purpose"  # Inside <I_002>
    ]

    if parent is not None:
        for key in elements_to_update:
            if key in updates:  # Only update if the key is in the updates dictionary
                element = parent.find(key)
                if element is not None:
                    if element.text != updates[key]:  # Only update if the value has changed
                        print(f"Updating {key} to {updates[key]}")  # Log the update
                        element.text = updates[key]  # Update the element value
                        updated = True
                    else:
                        print(f"{key} is already the same. No update needed.")
                else:
                    print(f"No element found for {key} inside {parent_tag}")

    return updated