import { FormCard } from '../components/FormCard';
import { RecipeForm } from '../components/RecipeForm';


export function RecipeAdd() {
    return (
        <FormCard
            title="Add a New Recipe"
            formComponent={< RecipeForm/>}
            buttonText="Add Recipe"
        />
    )
}
