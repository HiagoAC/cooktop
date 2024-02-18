import { FormCard } from '../components/FormCard';
import { SearchForm } from '../components/SearchForm';


export function RecipeSearch() {
    return (
        <FormCard
            title="Search for Recipes"
            formComponent={<SearchForm />}
            buttonText="Search"
        />
    )
}
