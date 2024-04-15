import { useState } from 'react';
import { Container } from 'react-bootstrap';
import { FormCard } from '../components/FormCard';
import { RecipeForm } from '../components/RecipeForm';
import { RequestAlert } from '../components/RequestAlert';
import { RecipeIn } from '../api/apiSchemas/recipesSchemas';
import { createRecipe, uploadImage } from '../api/recipesApi';
import { recipeTypes } from '../types/constants';


export function RecipeAdd() {
    const [recipe, setRecipe] = useState<RecipeIn>({
        title: '',
        time_minutes: null,
        tags: [],
        directions: [],
        description: null,
        recipe_type: recipeTypes['mai'],
        notes: null,
        ingredients: []
    });
    const [image, setImage] = useState<File | null>(null);
    const [
        createRecipeSuccess,
        setCreateRecipeSuccess
    ] = useState<boolean | null>(null);

    const handleAddRecipe = () => {
        createRecipe(recipe).then(res => {
            if (res.status === 201) {
                setCreateRecipeSuccess(true);
                if (image) {
                    const recipeId = res.data.id;
                    uploadImage(recipeId, image);
                }
            } else {
                setCreateRecipeSuccess(false);
            }
        });
    }
    return (
        <Container className="pb-4">
            <RequestAlert
                successCondition={createRecipeSuccess}
            />
            <FormCard
                title="Add a New Recipe"
                formComponent={
                    <RecipeForm
                        recipe={recipe}
                        setRecipe={setRecipe}
                        setImage={setImage}
                    />
                }
                buttonText="Add Recipe"
                handleClick={handleAddRecipe}
            />
        </Container>
    )
}
