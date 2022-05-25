#version 330
in vec2 v_texture;
in vec3 normal;
in vec3 fragPos;
out vec4 FragColor;

uniform vec3 lightPos;
uniform vec3 lightColor;

uniform float constant;
uniform float linear;
uniform float quadratic;

uniform mat4 rol;

uniform vec3 ambientColor;

uniform vec3 ambient;
uniform vec3 diffuse;
uniform vec3 specular;
uniform float shininess;

uniform vec3 cameraPos;

uniform sampler2D s_texture;

void main(){
    //attenuation
    vec3 lightPos_ = vec3(rol*vec4(lightPos,1));


    float distance = length(lightPos_ - fragPos);
    float attenuation = 1.0 / (constant + linear * distance + quadratic * (distance * distance));

    //diffuse
    vec3 norm = normalize(normal);
    vec3 lightDir = normalize(lightPos_ - fragPos);
    vec3 diffuse_ = diffuse * max(dot(norm, lightDir), 0.0) * lightColor;
    diffuse_ *= vec3(texture(s_texture, v_texture));

    //specular
    vec3 reflectVec = reflect(-lightDir,norm);
    vec3 cameraVec = normalize(cameraPos - fragPos);
    float specularAmount = pow(max(dot(reflectVec, cameraVec),0),shininess);
    vec3 specular_ = specular * specularAmount * lightColor;

    // ambient
    vec3 ambient_ =  ambientColor;

    ambient_ *= attenuation;
    diffuse_ *= attenuation;
    specular_ *= attenuation;

    FragColor = vec4((ambient_+diffuse_+specular_),1.0);

}