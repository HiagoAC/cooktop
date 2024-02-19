import { FormCard } from '../components/FormCard';
import { RecipeForm } from '../components/RecipeForm';


export function RecipeEdit() {
    return (
        <FormCard
            title="Edit Recipe"
            formComponent={< RecipeForm/>}
            buttonText="Save"
        />
    )
}
