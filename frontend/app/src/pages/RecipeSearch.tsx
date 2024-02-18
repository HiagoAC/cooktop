import { FormCard } from '../components/FormCard';
import { RecipeForm } from '../components/RecipeForm';


export function RecipeSearch() {
    return (
        <FormCard
            title="Search for Recipes"
            formComponent={< RecipeForm/>}
            buttonText="Search"
        />
    )
}
